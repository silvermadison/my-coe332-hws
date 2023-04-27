from flask import Flask, request, send_file
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
        This function will get, post, or delete a dataset about climate averages for various locations based on the method verb provided by the user.
        Returns:
            output_list (list): returns the dataset (for GET)
                OR
            (str) : stating that the data was loaded (for POST) or deleted (for DELETE)
    '''
    if request.method =='GET':
        output_list = []
        for item in rd.keys():
            output_list.append(json.loads(rd.get(item)))
        return output_list
    elif request.method =='POST':
        response = requests.get('https://raw.githubusercontent.com/michaelx/climate/master/climate.json')
        for item in response.json():
            key = "id"
            rd.set(item.get('id'),json.dumps(item))
        return "data loaded into redis"
    elif request.method == 'DELETE':
        rd.flushdb()
        return f"data deleted, there are {rd.keys()} keys in the database"
    else:
        return "the method you tried does not work"

@app.route('/countries', methods=['GET'])
def get_countries():
    '''
        This function gets a lsit of all the countries in the dataset
        Returns:
        countries (list): a list of countries in the climate dataset
    '''
    country_list = []
    alldata = []
    for item in rd.keys():
        alldata.append(json.loads(rd.get(item)))
    max_list = len(alldata)
    for x in range(max_list):
        country_list.append(alldata[x]['country'])
    countries = []
    for item in country_list:
        if item not in countries:
            countries.append(item)
    return countries

@app.route('/locations', methods=['GET'])
def get_cities():
    '''
        This function gets a list of all the cities in the climate dataset
        Returns:
        city_list (list): a list of cities in the dataset
    '''
    city_list = []
    alldata = []
    for item in rd.keys():
        alldata.append(json.loads(rd.get(item)))
    max_list = len(alldata)
    for x in range(max_list):
        city_list.append(alldata[x]['city'])
    return city_list

@app.route('/locations/<int:loc_num>', methods=['GET'])
def get_location_data(loc_num):
    '''
        This function returns all the information for 1 specific location given by a number from the user.
        Args:
            loc_num (int): the specific number (index) of the data set to look at
        Returns:
            climate_data[loc_num] (dict): a dictionary of location data include the ID, city, country, and monthlyAvg information for each month
    '''
    alldata = []
    for item in rd.keys():
        alldata.append(json.loads(rd.get(item)))
    if loc_num >= len(alldata):
        return "Error: Location value is not in the data set" , 400
    return alldata[loc_num]

@app.route('/locations/<int:loc_num>/high-month', methods=['GET'])
def get_month_high(loc_num):
    '''
        This function returns the monthly average high tempature for 1 specific location given by a number from the user.
        Args:
            loc_num (int): the specific number (index) of the data set to look at
        Returns:
            highT (list): a list of the average high temperatures for each month in order for the chosen location
    '''
    highT = []
    alldata = []
    for item in rd.keys():
        alldata.append(json.loads(rd.get(item)))
    if loc_num >= len(alldata):
        return "Error: Location value is not in the data set" , 400
    for x in range(12):
        highT.append(alldata[loc_num]['monthlyAvg'][x]['high'])
    return highT

@app.route('/locations/<int:loc_num>/high-year', methods=['GET'])
def get_yr_high(loc_num):
    '''
        This function returns the high temperature year average for 1 specific location given by a number from the user.
        Args:
            loc_num (int): the specific number (index) of the data set to look at
        Returns:
            yr_highT (int): the average high temperature for the chosen location for the year
    '''
    alldata = []
    for item in rd.keys():
        alldata.append(json.loads(rd.get(item)))
    if loc_num >= len(alldata):
        return "Error: Location value is not in the data set" , 400
    highT_list = get_month_high(loc_num)
    sum = 0
    for x in highT_list:
        sum = sum+x
    yr_highT = sum/12
    num = str(yr_highT)
    units= " degrees celsius"
    return num+units

@app.route('/locations/<int:loc_num>/high-month/plot', methods=['GET', 'POST', 'DELETE'])
def get_high_plot(loc_num):
    '''
    This function will get, post, or delete an image from the dataset based on the method verb provided by the user.
    Returns:
        image(png): histogram of the average high temperatures by month for a given location num/ID
        OR
        (str): stating the the image in the database has been posted or deleted
    '''
    alldata = []
    if request.method == 'GET':
        if rd_img.exists('highT_avs'):
            with open('./highT_avs.png', 'wb') as f:
                f.write(rd_img.get('highT_avs'))
            return send_file('./highT_avs.png', minetype='highT_avs/png', as_attachment=True)#send image to user
        else:
            return 'there is no image in the database'

    elif request.method == 'POST':
        for item in rd.keys():
            alldata.append(json.loads(rd.get(item)))
        if loc_num >= len(alldata):
            return "Error: Location value is not in the data set" , 400
        highT = get_month_high(loc_num)
        plt.hist(highT, 5)
        title = f'Average High Temperatures in {alldata[loc_num]["city"]}'
        plt.title(title)
        plt.xlabel('Months (Jan to Dec)')
        plt.ylabel('Temperature in Celsius')
        plt.savefig('./highT_avs.png')
        filebytes = open('./highT_avs.png','rb').read()
        rd_img.set('highT_avs', filebytes)
        return 'the image has been uploaded to the database.\n'

    elif request.method == 'DELETE':
        rd_img.flushdb()
        return 'the image has been deleted from the database'
    
    else:
        return 'error in requested method', 400

 #--------------------------------------- low temp routes -----------------------------

@app.route('/locations/<int:loc_num>/low-month', methods=['GET'])
def get_month_low(loc_num):
    '''
        This function returns the monthly average low tempatures for 1 specific location given by a number from the user.
        Args:
            loc_num (int): the specific number (index) of the data set to look at
        Returns:
            highT (list): a list of the average low temperatures for each month in order for the chosen location
    '''
    lowT = []
    alldata = []
    for item in rd.keys():
        alldata.append(json.loads(rd.get(item)))
    if loc_num >= len(alldata):
        return "Error: Location value is not in the data set" , 400
    for x in range(12):
        lowT.append(alldata[loc_num]['monthlyAvg'][x]['low'])
    return lowT

@app.route('/locations/<int:loc_num>/low-year', methods=['GET'])
def get_yr_low(loc_num):
    '''
        This function returns the low temperature year average for 1 specific location given by a number from the user.
        Args:
            loc_num (int): the specific number (index) of the data set to look at
        Returns:
            yr_highT (int): the average low temperature for the chosen location for the year
    '''
    alldata = []
    for item in rd.keys():
        alldata.append(json.loads(rd.get(item)))
    if loc_num >= len(alldata):
        return "Error: Location value is not in the data set" , 400
    lowT_list = get_month_low(loc_num)
    sum = 0
    for x in lowT_list:
        sum = sum+x
    yr_lowT = sum/12
    num = str(yr_lowT)
    units= " degrees celsius"
    return num+units

@app.route('/locations/<int:loc_num>/low-month/plot', methods=['GET', 'POST', 'DELETE'])
def get_low_plot(loc_num):
    '''
    This function will get, post, or delete an image from the dataset based on the method verb provided by the user.
    Returns:
        image(png): histogram of the average low temperatures by month for a given location num/ID
        OR
        (str): stating the the image in the database has been posted or deleted
    '''
    alldata = []
    if request.method == 'GET':
        if rd_img.exists('lowT_avs'):
            with open('./lowT_avs.png', 'wb') as f:
                f.write(rd_img.get('lowT_avs'))
            return send_file('./lowT_avs.png', minetype='lowT_avs/png', as_attachment=True)#send image to user
        else:
            return 'there is no image in the database'

    elif request.method == 'POST':
        for item in rd.keys():
            alldata.append(json.loads(rd.get(item)))
        if loc_num >= len(alldata):
            return "Error: Location value is not in the data set" , 400
        lowT = get_month_low(loc_num)
        plt.hist(lowT, 5)
        title = f'Average Low Temperatures in {alldata[loc_num]["city"]}'
        plt.title(title)
        plt.xlabel('Months (Jan to Dec)')
        plt.ylabel('Temperature in Celsius')
        plt.savefig('./lowT_avs.png')
        filebytes = open('./lowT_avs.png','rb').read()
        rd_img.set('lowT_avs', filebytes)
        return 'the image has been uploaded to the database.\n'

    elif request.method == 'DELETE':
        rd_img.flushdb()
        return 'the image has been deleted from the database'
    
    else:
        return 'error in requested method', 400
    
    
#--------------------------------------- dry day routes -----------------------------

@app.route('/locations/<int:loc_num>/dry-month', methods=['GET'])
def get_month_dry(loc_num):
    '''
        This function returns the monthly average dry days for 1 specific location given by a number from the user.
        Args:
            loc_num (int): the specific number (index) of the data set to look at
        Returns:
            dry (list): a list of the average dry days for each month in order for the chosen location
    '''
    dry = []
    alldata = []
    for item in rd.keys():
        alldata.append(json.loads(rd.get(item)))
    if loc_num >= len(alldata):
        return "Error: Location value is not in the data set" , 400
    for x in range(12):
        dry.append(alldata[loc_num]['monthlyAvg'][x]['dryDays'])
    return dry

@app.route('/locations/<int:loc_num>/dry-year', methods=['GET'])
def get_yr_dry(loc_num):
    '''
        This function returns the average number of dry days a year for 1 specific location given by a number from the user.
        Args:
            loc_num (int): the specific number (index) of the data set to look at
        Returns:
            yr_dry (int): the average nunmber of dry days for the chosen location for the year
    '''
    alldata = []
    for item in rd.keys():
        alldata.append(json.loads(rd.get(item)))
    if loc_num >= len(alldata):
        return "Error: Location value is not in the data set" , 400
    dry_list = get_month_dry(loc_num)
    sum = 0
    for x in dry_list:
        sum = sum+x
    yr_dry = sum/12
    num = str(yr_dry)
    units = " days"
    return num +units

@app.route('/locations/<int:loc_num>/dry-month/plot', methods=['GET', 'POST', 'DELETE'])
def get_dry_plot(loc_num):
    '''
    This function will get, post, or delete an image from the dataset based on the method verb provided by the user.
    Returns:
        image(png): histogram of the average number of dry days by month for a given location num/ID
        OR
        (str): stating the the image in the database has been posted or deleted
    '''
    alldata = []
    if request.method == 'GET':
        if rd_img.exists('dry_avs'):
            with open('./dry_avs.png', 'wb') as f:
                f.write(rd_img.get('dry_avs'))
            return send_file('./dry_avs.png', minetype='dry_avs/png', as_attachment=True)
        else:
            return 'there is no image in the database'

    elif request.method == 'POST':
        for item in rd.keys():
            alldata.append(json.loads(rd.get(item)))
        if loc_num >= len(alldata):
            return "Error: Location value is not in the data set" , 400
        dry = get_month_dry(loc_num)
        plt.hist(dry, 10)
        title = f'Average Dry Days in {alldata[loc_num]["city"]}'
        plt.title(title)
        plt.xlabel('Months (Jan to Dec)')
        plt.ylabel('Number of Days')
        plt.savefig('./dry_avs.png')
        filebytes = open('./dry_avs.png','rb').read()
        rd_img.set('dry_avs', filebytes)
        return 'the image has been uploaded to the database.\n'

    elif request.method == 'DELETE':
        rd_img.flushdb()
        return 'the image has been deleted from the database'
    
    else:
        return 'error in requested method', 400
    
 #--------------------------------------- snow day routes -----------------------------

@app.route('/locations/<int:loc_num>/snow-month', methods=['GET'])
def get_month_snow(loc_num):
    '''
        This function returns the monthly average snow days for 1 specific location given by a number from the user.
        Args:
            loc_num (int): the specific number (index) of the data set to look at
        Returns:
            snow (list): a list of the average snow days for each month in order for the chosen location
    '''
    alldata = []
    snow = []
    for item in rd.keys():
        alldata.append(json.loads(rd.get(item)))
    if loc_num >= len(alldata):
        return "Error: Location value is not in the data set" , 400
    for x in range(12):
        snow.append(alldata[loc_num]['monthlyAvg'][x]['snowDays'])
    return snow

@app.route('/locations/<int:loc_num>/snow-year', methods=['GET'])
def get_yr_snow(loc_num):
    '''
        This function returns the average number of snow days a year for 1 specific location given by a number from the user.
        Args:
            loc_num (int): the specific number (index) of the data set to look at
        Returns:
            yr_snow (int): the average nunmber of snow days for the chosen location for the year
    '''
    alldata = []
    for item in rd.keys():
        alldata.append(json.loads(rd.get(item)))
    if loc_num >= len(alldata):
        return "Error: Location value is not in the data set" , 400
    snow_list = get_month_snow(loc_num)
    sum = 0
    for x in snow_list:
        sum = sum+x
    yr_snow = sum/12
    num = str(yr_snow)
    units = " days"
    return num +units

@app.route('/locations/<int:loc_num>/snow-month/plot', methods=['GET', 'POST', 'DELETE'])
def get_snow_plot(loc_num):
    '''
    This function will get, post, or delete an image from the dataset based on the method verb provided by the user.
    Returns:
        image(png): histogram of the average number of snow days by month for a given location num/ID
        OR
        (str): stating the the image in the database has been posted or deleted
    '''
    alldata = []
    if request.method == 'GET':
        if rd_img.exists('snow_avs'):
            with open('./snow_avs.png', 'wb') as f:
                f.write(rd_img.get('snow_avs'))
            return send_file('./snow_avs.png', minetype='snow_avs/png', as_attachment=True)
        else:
            return 'there is no image in the database'

    elif request.method == 'POST':
        for item in rd.keys():
            alldata.append(json.loads(rd.get(item)))
        if loc_num >= len(alldata):
            return "Error: Location value is not in the data set" , 400
        snow = get_month_snow(loc_num)
        plt.hist(snow, 3)
        title = f'Average Number of Snow Days in {alldata[loc_num]["city"]}'
        plt.title(title)
        plt.xlabel('Months (Jan to Dec)')
        plt.ylabel('Number of Days')
        plt.savefig('./lowT_avs.png')
        filebytes = open('./snow_avs.png','rb').read()
        rd_img.set('snow_avs', filebytes)
        return 'the image has been uploaded to the database.\n'

    elif request.method == 'DELETE':
        rd_img.flushdb()
        return 'the image has been deleted from the database'
    
    else:
        return 'error in requested method', 400
    
    #--------------------------------------- rainfall routes -----------------------------

@app.route('/locations/<int:loc_num>/rainfall-month', methods=['GET'])
def get_month_rainfall(loc_num):
    '''
        This function returns the monthly average rainfall for 1 specific location given by a number from the user.
        Args:
            loc_num (int): the specific number (index) of the data set to look at
        Returns:
            rainfall (list): a list of the average rainfall for each month in order for the chosen location
    '''
    rain = []
    alldata = []
    for item in rd.keys():
        alldata.append(json.loads(rd.get(item)))
    if loc_num >= len(alldata):
        return "Error: Location value is not in the data set" , 400
    for x in range(12):
        rain.append(alldata[loc_num]['monthlyAvg'][x]['rainfall'])
    return rain

@app.route('/locations/<int:loc_num>/rainfall-year', methods=['GET'])
def get_yr_rainfall(loc_num):
    '''
        This function returns the average rainfall a year for 1 specific location given by a number from the user.
        Args:
            loc_num (int): the specific number (index) of the data set to look at
        Returns:
            yr_rainfall (int): the average rainfall for the chosen location for the year
    '''
    alldata = []
    for item in rd.keys():
        alldata.append(json.loads(rd.get(item)))
    if loc_num >= len(alldata):
        return "Error: Location value is not in the data set" , 400
    rain_list = get_month_low(loc_num)
    sum = 0
    for x in rain_list:
        sum = sum+x
    yr_rain = sum/12
    num = str(yr_rain)
    units = " millimeters"
    return num+units

@app.route('/locations/<int:loc_num>/rainfall-month/plot', methods=['GET', 'POST', 'DELETE'])
def get_rainfall_plot(loc_num):
    '''
    This function will get, post, or delete an image from the dataset based on the method verb provided by the user.
    Returns:
        image(png): histogram of the average rainfall by month for a given location num/ID
        OR
        (str): stating the the image in the database has been posted or deleted
    '''
    alldata = []
    if request.method == 'GET':
        if rd_img.exists('rain_avs'):
            with open('./rain_avs.png', 'wb') as f:
                f.write(rd_img.get('rain_avs'))
            return send_file('./rain_avs.png', minetype='rain_avs/png', as_attachment=True)
        else:
            return 'there is no image in the database'

    elif request.method == 'POST':
        for item in rd.keys():
            alldata.append(json.loads(rd.get(item)))
        if loc_num >= len(alldata):
            return "Error: Location value is not in the data set" , 400
        rain = get_month_rainfall(loc_num)
        plt.hist(rain, 20)
        title = f'Average Number of Rainy Days in {alldata[loc_num]["city"]}'
        plt.title(title)
        plt.xlabel('Months (Jan to Dec)')
        plt.ylabel('Rainfall in mm')
        plt.savefig('./rain_avs.png')
        filebytes = open('./rain_avs.png','rb').read()
        rd_img.set('rain_avs', filebytes)
        return 'the image has been uploaded to the database.\n'

    elif request.method == 'DELETE':
        rd_img.flushdb()
        return 'the image has been deleted from the database'
    
    else:
        return 'error in requested method', 400
    
#-------------------------------- overall yearly average ----------------------
@app.route('/locations/<int:loc_num>/year', methods=['GET'])
def get_yrly_avs(loc_num):
    '''
        This function returns the cliamtes yearly averages for 1 specific location given by a number from the user.
        Args:
            loc_num (int): the specific number (index) of the data set to look at
        Returns:
            yr_avs (dict): a dictionary of the averages for the year which includes highTemp, lowTemp, dryDays, snowDays, and rainfall
    '''
    yr_avs = {}
    yr_avs['highTemp'] = get_yr_high(loc_num)
    yr_avs['lowTemp']= get_yr_low(loc_num)
    yr_avs['dryDays']= get_yr_dry(loc_num)
    yr_avs['snowDays']= get_yr_snow(loc_num)
    yr_avs['rainfall']= get_yr_rainfall(loc_num)
    return yr_avs

#------------------------------------help route-----------------------
@app.route('/help', methods=['GET'])
def all_routes():
    '''
        This function returns a list of all the possible routes in this API and a short description of what they each return.
     Returns:
            (str): a string with routes and what they return
    '''
    welcome = "Welcome to Help! Below are available routes and their return statements. \n \n"
    r1 = ("The route '/data' returns, posts, or deletes the entire data set based on the verb given. \n") 
    r2 = ("The route '/countries' returns a list of all the countries in the data set. \n") 
    r3= ("The route '/locations' returns a list of epochs in the data set between offset and limit. If offset is not given then the list will start at the first epoch and if limit is not given the list will end at the last epoch. \n")
    r4 =("The route '/locations/<loc_num>' returns a dictionary of the specific epoch data set requested with unique keys about its position and velocity data. \n")
    r5 = ("The route '/locations/<loc_num>/high-month' returns the average high temperatures for each month given a specific location number/id in the dataset \n")
    r6 =("The route '/locations/<loc_num>/high-year' returns the yearly average high temperature for a specific location number/id in the dataset \n")
    r7 =("The route '/locations/<loc_num>/low-month' returns the average low temperatures for each month given a specific location number/id in the dataset \n")
    r8 = ("The route '/locations/<loc_num>/low-year' returns the yearly average low temperature for a specific location number/id in the dataset \n")
    r9 = ("The route '/locations/<loc_num>/dry-month' returns the average number of dry days for each month given a specific location number/id in the dataset  \n")
    r10 = ("The route '/locations/<loc_num>/dry-year' returns the yearly number of dry days for a specific location number/id in the dataset \n")
    r11 = ("The route '/locations/<loc_num>/snow-month' returns the average number of snow days for each month given a specific location number/id in the dataset \n")
    r12 = ("The route '/locations/<loc_num>/snow-year' returns the yearly number of snow days for a specific location number/id in the dataset \n")
    r13 = ("The route '/locations/<loc_num>/rainfall-month' returns the average rainfall for each month given a specific location number/id in the dataset \n")
    r14 = ("The route '/locations/<loc_num>/rainfall-year' returns the yearly rainfall for a specific location number/id in the dataset \n")
    r15 = ("The route '/locations/<loc_num>/year' returns the cliamtes yearly averages for a specific location number/id in the dataset \n")
    r16 = ("The route '/locations/<loc_num>/high-month/plot' returns, posts, or deletes a histogram image of the monthly average high temperatures for a given location number/id based on the verb given. \n") 
    r17 = ("The route '/locations/<loc_num>/low-month/plot' returns, posts, or deletes a histogram image of the monthly average low temperatues for a given location number/id based on the verb given. \n") 
    r18 = ("The route '/locations/<loc_num>/dry-month/plot' returns, posts, or deletes a histogram image of the monthly average number of dry days for a given location number/id based on the verb given. \n") 
    r19 = ("The route '/locations/<loc_num>/snow-month/plot' returns, posts, or deletes a histogram image of the monthly average number of snow for a given location number/id based on the verb given. \n") 
    r20 = ("The route '/locations/<loc_num>/rainfall-month/plot' returns, posts, or deletes a histogram image of the monthly average rainfall for a given location number/id based on the verb given. \n")     
    return welcome +r1 + r2 +r3 +r4 +r5 +r6+r7+r8+r9+r10+r11+r12+r13+r14+r15+r16+r17+r18+r19+r20


#______________________end of routes________________________
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
