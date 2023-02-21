import requests
import xmltodict
import math
from flask import Flask

app = Flask(__name__)

def get_data():
    '''
        This functions gets the position and velocity data from the ISS

        Returns:
            data (dict): a dictionary of ISS data with the same keys
    '''
    url = "https://nasa-public-data.s3.amazonaws.com/iss-coords/current/ISS_OEM/ISS.OEM_J2K_EPH.xml"
    response = requests.get(url)
    info = xmltodict.parse(response.text)
    data = info['ndm']['oem']['body']['segment']['data']['stateVector']
    return data

@app.route('/', methods = ['GET'])
def get_data_set():
    '''
        This function gets the entire ISS data set that we are using

        Returns:
        data (dict): a dictionary of usable ISS data with the same keys
    '''
    data = get_data()
    return data

@app.route('/epochs', methods = ['GET'])
def get_epochs_data():
    '''
        This function returns only a list of epochs which is a key name.

        Returns:
            epoch_list(list): a list of epoch data
    '''
    data = get_data()
    epoch_list = []
    length = len(data)
    for i in range(length):
        epoch_list.append( data[i]['EPOCH'] )
    return epoch_list

@app.route('/epochs/<int:epoch>', methods = ['GET'])
def get_an_epoch_data(epoch):
    '''
        This function finds the data of a specific epoch/data set.

        Args:
            epoch (int): the specific number of the data set to look at

        Returns:
            data[epoch] (dict): a dictionary of the specific data set requested with unique keys about its position and velocity data
    '''
    data = get_data()
    #attempted exception handling, but recieved errors
    #try:
    #    epoch<len(data)
    #except IndexError:
    #    return "Error: Epoch value is not in the data set", 400
    if epoch>=len(data):
        return "Index Error: Epoch value is not in the data set" , 400
    return data[epoch]

@app.route('/epochs/<int:epoch>/speed', methods = ['GET'])
def get_speed(epoch):
    '''
        This function finds the speed of a given epoch.

        Args:
            epoch (int): the specific number of the data set to look at

        Returns:
            speed (float): the instantaneous speed of the given epoch
    '''
    data = get_data()
    #if epoch is not in data - same format as in get_an_epoch_data function
    if epoch>=len(data):
        return "Error: Epoch value is not in the data set", 400
    #use speed eq
    xdot = data[epoch]['X_DOT']['#text'] 
    ydot = data[epoch]['Y_DOT']['#text'] 
    zdot = data[epoch]['Z_DOT']['#text'] 
    xdot = float(xdot)
    ydot = float(ydot)
    zdot = float(zdot)
    calc = (xdot*xdot)+(ydot*ydot)+(zdot*zdot)
    speed = math.sqrt(calc )
    units = data[epoch]['X_DOT']['@units']
    #return str(speed)
    return (f'speed: {str(speed)} {units}')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')






