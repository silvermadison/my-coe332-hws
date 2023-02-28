# Homework 05
## Objective
The purpose of this assignment is to practice software design including REST APIs (Representational State Transfer Application Programming Interfaces), the Flask Application, creating routes in Flask using type annotations and docstrings, working with XML data, and containerization. 

## Contents
This folder includes 1 script, 1 Dockerfile, and 1 README file.

## ISS Data
The International Space Station (ISS) data is a dictionary of data points with epoch, position, and velocity data with a name EPOCH and keys X, X_DOT, Y, Y_DOT, Z, Z_DOT. The ISS information can be found at their website (https://spotthestation.nasa.gov/trajectory_data.cfm).

Keeter, Bill. “ISS Trajectory Data.” Edited by Jacob Keaton, *Spot the Station International Space Station*, NASA, 27 July 2021, https://spotthestation.nasa.gov/trajectory_data.cfm. 

### Part 1 - Routes
In the ```iss_tracker.py``` file, it contains instructions for reading the ISS data and the app routes below. The requests and xmltodict modules are used to read the ISS information into a usable dictionary of the data. 

| Route | Method | What it should return | 
| ---------------------------- | ---------------------------- | ---------------------------- |
| ```/``` | GET | the entire data set |
| ```/epochs``` | GET |  a list of all epochs in the set | 
| ```/epochs?limit=int&offset=int``` | GET | a modified list of epochs given query parameters | 
| ```/epochs/<epoch>``` | GET | data for a specific Epoch from the data set |
| ```/epochs/<epoch>/speed``` | GET | instantaneous speed for a specific Epoch in the data set  |
| ```/help``` | GET | a help text (as a string) that briefly describes each route |
| ```/delete-data``` | DELETE | delete all data from the dictionary object |
| ```/post-data``` | POST | reload the dictionary object with data from the web |

In order to find the speed in the ```/epochs/<epoch>/speed``` route the following equation was used:
speed = sqrt(x_dot^2 + y_dot^2 + z_dot^2)


### Part 2 - Dockerfile 
The Dockerfile contains commands for building a new image. When creating the Dockerfile the image should contain the same versions of modules as you are using on the Jetstream VM; this will be reflected in the ```FROM``` and ```RUN``` instructions. We will do this for the modules python, flask, requests, and xmltodict.

To check your version of python run ```python3``` in the VM command line. Output should look similar to:
```
Python 3.8.10 (default, Nov 14 2022, 12:59:47) 
[GCC 9.4.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> 
```
The first line shows you the version of python you are using, in this case I am using Python 3.8.10. This same version is contained in the ```FROM``` instruction in the Dockerfile.

To check your version of flask, in the VM command line run ```pip freeze | grep Flask```. Output should look similar to:
```
Flask==2.2.2
```
The version of Flask I am using is 2.2.2 and this version is also used in the ```RUN``` instruction in the Dockerfile.

To check your version of requests, in the VM command line run ```pip freeze | grep requests```. Output should look similar to:
```
requests==2.22.0
```
The version of requests I am using is 2.22.0 and this version is also used in the ```RUN``` instruction in the Dockerfile.

To check your version of xmltodict, in the VM command line run ```pip freeze | grep xmltodict```. Output should look similar to:
```
xmltodict==0.13.0
```
The version of xmltodict I am using is 0.13.0 and this version is also used in the ```RUN``` instruction in the Dockerfile.


## Instructions
### Pull the Image from Docker Hub
To get the image from Docker Hub use the command ```docker pull silvermadison/iss_tracker:hw05```.


### Build a New Image from This Dockerfile
In order to retrieve the data from this repository use the command
```
git clone git@github.com:silvermadison/my-coe332-hws.git
```
This will provide you with all the data in this repository. Navigate to the homework05 folder to access its contents so you can follow along with this assignment.

Create the image using the command ```docker build -t silvermadison/iss_tracker:hw05 .```.

Check to make sure the image is there using the command```docker images```. Output should look like:
```
REPOSITORY                  TAG       IMAGE ID       CREATED          SIZE
silvermadison/iss_tracker   hw05      9b88163e71e8   7 minutes ago    897MB
```

### Run the Containerized Flask App
Test the image with the command ```docker run -it --rm silvermadison/iss_tracker:hw05 /bin/bash```.
Once this is run you should be in the container. From here you can go into the python interpreter to ensure the flask, requests, and xmltodict modules have been installed with no errors. This exchange should look like the following:
```
root@9a1f45a8ea52:/# python
Python 3.8.10 (default, Jun 23 2021, 15:19:53) 
[GCC 8.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import flask
>>> import requests
>>> import xmltodict
>>> 
```
Quit the python interpreter with ```quit()``` and then run Flask in the container ```flask --app iss_tracker --debug run```.

### Example Outputs and API Query Commands
Now with the container running, you can test API query commands. In order to run the code, open another tab in your linux operating system so that you have two tabs total. In one tab the container is running in the foreground and in the other tab API query commands will be made.

The ```/``` route should output the entire ISS dataset:
```
[
  {
    "EPOCH": "2023-048T12:00:00.000Z",
    "X": {
      "#text": "-5097.51711371908",
      "@units": "km"
    },
    "X_DOT": {
      "#text": "-4.5815461024513304",
      "@units": "km/s"
    },
    "Y": {
      "#text": "1610.3574036042901",
      "@units": "km"
    },
    "Y_DOT": {
      "#text": "-4.8951801207083303",
      "@units": "km/s"
    },
    "Z": {
      "#text": "-4194.4848049601396",
      "@units": "km"
    },
    "Z_DOT": {
      "#text": "3.70067961081915",
      "@units": "km/s"
    }
  },
  {
    "EPOCH": "2023-048T12:04:00.000Z",
    "X": {
      "#text": "-5998.4652356788401",
      "@units": "km"
    },
    "X_DOT": {
      "#text": "-2.8799691318087701",
      "@units": "km/s"
    },
    "Y": {
      "#text": "391.26194859011099",
      "@units": "km"
    },
    "Y_DOT": {
      "#text": "-5.2020406581448801",
      "@units": "km/s"
    },
    "Z": {
      "#text": "-3164.26047476555",
      "@units": "km"
    },
    "Z_DOT": {
      "#text": "4.8323394499086101",
      "@units": "km/s"
    }
  },
…
]
```

The ```/epochs``` route should output a list of all the epochs in the data set: 
```
[
  "2023-048T12:00:00.000Z",
  "2023-048T12:04:00.000Z",
  "2023-048T12:08:00.000Z",
  "2023-048T12:12:00.000Z",
  "2023-048T12:16:00.000Z",
…
]
```


Some example output for the limit and offset query parameters are below. 

Test the limit parameter with the command ```curl localhost:5000/epochs?limit=10```. The output should be a total of 10 epochs:
```
[
  "2023-055T12:00:00.000Z",
  "2023-055T12:04:00.000Z",
  "2023-055T12:08:00.000Z",
  "2023-055T12:12:00.000Z",
  "2023-055T12:16:00.000Z",
  "2023-055T12:20:00.000Z",
  "2023-055T12:24:00.000Z",
  "2023-055T12:28:00.000Z",
  "2023-055T12:32:00.000Z",
  "2023-055T12:36:00.000Z"
]
```

To use both parameters together you must run the ```curl``` a little differently: ```curl 'localhost:5000/epochs?limit=3&offset=2'```. The output should start the epochs list on the 3rd epoch (offset by 2) and have the next 3 epochs:
```
[
  "2023-055T12:08:00.000Z",
  "2023-055T12:12:00.000Z",
  "2023-055T12:16:00.000Z"
]
```


The ```/epochs/1``` route should output the positional and velocity data for a specific epoch: 
```
{
  "EPOCH": "2023-048T12:04:00.000Z",
  "X": {
    "#text": "-5998.4652356788401",
    "@units": "km"
  },
  "X_DOT": {
    "#text": "-2.8799691318087701",
    "@units": "km/s"
  },
  "Y": {
    "#text": "391.26194859011099",
    "@units": "km"
  },
  "Y_DOT": {
    "#text": "-5.2020406581448801",
    "@units": "km/s"
  },
  "Z": {
    "#text": "-3164.26047476555",
    "@units": "km"
  },
  "Z_DOT": {
    "#text": "4.8323394499086101",
    "@units": "km/s"
  }
}
```

The ```/epochs/1/speed``` route should output the instantaneous speed for a specific epoch:
```
speed: 7.662046317290625 km/s
```


For the ```/help``` route the output should be an explanation of all the routes and their outputs:
```
Welcome to Help! Below are available routes and their return statements. 

The route '/' returns the entire data set. 
The route '/epochs' returns a list of all the epochs in the data set.
The route '/epochs?limit=int&offset=int' returns a list of epochs in the data set between offset and limit. If offset is not given then the list will start at the first epoch and if limit is not given the list will end at the last epoch.
The route '/epochs/<epoch>' returns a dictionary of the specific epoch data set requested with unique keys about its position and velocity data.
The route '/epochs/<epoch>/speed' returns the instantaneous speed for a specific epoch in the data set.
The route '/delete-data' deletes all data from the data set. 
The route '/post-data' reloads the dictionary with data from the web.
```

In order to run the ```/delete-data``` route you must run the ```curl``` a little differently: ```curl -X DELETE localhost:5000/delete-data```. The output should be an empty dataset since it deletes the data:
```
[]
```
Check that the data set has actually been deleted by running ```curl localhost:5000/```.


The same unique curl command is the case for the ```/post-data``` route. Use the command ```curl -X POST localhost:5000/post-data```. Output:
```
the data has been posted
```
Check that the data set has actually been posted by running ```curl localhost:5000/```.


