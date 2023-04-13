from flask import Flask, request
import requests
import redis
import json
import os
from matplotlib import pyplot as plt
import numpy as np

app = Flask(__name__)
def get_redis_client(db_numb:int,decode_ans:bool):
    '''
    This function connects to the redis database
    '''
    redis_ip = os.environ.get('REDIS_IP')
    if not redis_ip:
        raise Exception()
    return redis.Redis(host=redis_ip, port=6379, db=db_numb, decode_responses=decode_ans)
rd = get_redis_client(0, True)
rd_img = get_redis_client(1, False)

@app.route('/data', methods=['POST','GET','DELETE'])
def handle_data():
    '''
        This function will get, post, or delete a dataset about genes based on the method verb provided by the user.

        Returns:
            output_list (list): returns the dataset (for GET) 
                OR
            (string) : stating that the data was loaded (for POST) or deleted (for DELETE)
    '''
    if request.method =='GET':
        output_list = []
        for item in rd.keys():
            output_list.append(json.loads(rd.get(item)))
        return output_list
    elif request.method =='POST':
        response = requests.get('https://ftp.ebi.ac.uk/pub/databases/genenames/hgnc/json/hgnc_complete_set.json')
        for item in response.json()['response']['docs']:
            key = f'{item["hgnc_id"]}'
            rd.set(item.get('hgnc_id'),json.dumps(item))
        return "data loaded into redis"
    elif request.method == 'DELETE':
        rd.flushdb()
        return f"data deleted, there are {rd.keys()} keys in the database"
    else:
        return "the method you tried does not work"

@app.route('/genes', methods=['GET'])
def get_genes():
    '''
        This functions returns a list of all hgnc_ids.

        Returns:
            gene_list(list): list of all genes in the database
    '''
    gene_list = []
    for item in rd.keys():
        if item == 'hgnc_id':
            gene_list.append(item)
    return gene_list

@app.route('/genes/<int:hgnc_id>', methods=['GET'])
def get_gene_info(id_num):
    '''
        This functions returns all the data associated with a given hgnc_id provided by the user.

        Returns:
            gene_info (dict): information about the specific gene id
    '''
    id_str = "HGNC:"+id_num
    alldata = []
    gene_info = []
    for item in rd.keys():
        alldata.append()json.loads(rd.get(item)))
    for point in alldata:
        if point == id_str:
            gene_info = json.dumps(point)
    return gene_info

@app.route('/image', methods=['GET', 'POST', 'DELETE'])
def get_image():
    """
    This function will get, post, or delete an image from the dataset based on the method verb provided by the user.
    
    Returns:
        image(png): histogram of the amount of genes in each gene group id
        OR
        (str): stating the the image in the database has been posted or deleted
    """
    if request.method == 'GET':
        if rd.exists('image'):
            with open('./image.png', 'wb') as f:
                f.write(rd_img.get('image'))
            return send_file('./image.png', minetype='image/png', as_attachment=True)#send image to user
        else:
            return 'there is no image in the database'
    elif request.method == 'POST':
        if len(rd.keys())==0:
            return 'not enough data in the database'
        genes=[]
        data=[]
        gene_grp={}
        for item in rd.keys():
            item = json.loads(rd.get(item))
            if item['gene_group_id'] not in gene_grp:
                gene_grp[item['gene_group_id']]=1
            else:
                gene_grp[item['gene_group_id']]+=1
        for key in gene_grp.keys():
            genes.append(key)
            data.append(item[key])
        plt.figure()
        plt.plot(data,100, labels=genes)
        plt.xlabel('Gene Group IDs')
        plt.ylabel('Numbers of Genes')
        plt.title('Gene Group IDs in Dataset')
        plt.savefig('./image.png')
        filebytes = open('./image.png','rb').read()
        rd.set('image', filebytes)
        return 'the image has been uploaded to the database.\n'
    elif request.method == 'DELETE':
        rd.flushdb()
        return 'the image has been deleted from the database'
    else:
        return 'error in requested method', 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')


