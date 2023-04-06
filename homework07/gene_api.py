from flask import Flask, request
import requests
import redis
import json

app = Flask(__name__)
def get_redis_client():
    return redis.Redis(host='127.0.0.1', port=6379, db=0, decode_responses=True)
rd = get_redis_client()

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
        return f"data deleted, there are {rd.keys()} in the database"
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


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')


