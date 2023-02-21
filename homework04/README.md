# Homework 4: ISS Data

## Objective
The key takeaway from this project is to practice software design including REST APIs (Representational State Transfer Application Programming Interfaces), the Flask Application, creating routes in Flask using type annotations and docstrings, and working with XML data. The contents of this folder includes 1 script and 1 README file.

## Requirements

This program requires importing the math module and requests, xmltodict, and flask libraries. Follow instructions below to install necessary components.

Install the library xmltodict: 
```
pip3 install --user xmltodict
```


Install the requests library:
```
pip3 install --user requests
```

Install the flask library:
```
pip3 install --user flask
```

## ISS Data
Given International Space Station (ISS) positional and velocity data, the task is to build a Flask application for querying and returning interesting information from the ISS data set.

### Task 1 - Read the Data
The ISS positional and velocity data can be found at their website (https://spotthestation.nasa.gov/trajectory_data.cfm).
Using the XML data, the function ```get_data``` reads this information into a usable dictionary of the data we are trying to find.

### Task 2 - Query the ISS Data Using Flask
Using the data populated from Task 1, return the following data for the following routes:
| Route | What it should return | 
| ---------------------------- | ---------------------------- |
| ```/``` | the entire data set |
| ```/epoch``` | a list of all epochs in the set | 
| ```/epoch/<epoch>``` | data for a specific Epoch from the data set |
| ```/epoch/<epoch>/speed``` | instantaneous speed for a specific Epoch in the data set  |

In order to find the speed in the last route the following equation was used:
speed = sqrt(x_dot^2 + y_dot^2 + z_dot^2)

## Cloning the Repository
In order to retrieve the data from this repository use the command
```
git clone git@github.com:silvermadison/my-coe332-hws.git
```
This will provide you with all the data in this repository. Make sure you move to the homework04 folder to access its contents so you can follow along with this assignment.

## Running the Code
Now that you have the application and code, you can run the code. In order to run the code, open another tab in your linux operating system so that you have two tabs total. 
In one tab we will run the Flask application, using the command line below, so we can leave it in the foreground while working in the other tab. The server will automatically update as we are working in the other tab. 
```
flask --app iss_tracker --debug run
```

In the other tab, **not** running the Flask application, we will run commands to test the code. Using the ```curl``` command we will talk to the server. The server is listening on the ```local host``` on the default flask port ```5000```. To make a request to the Flask application our statement will follow the format:
```
curl localhost:5000
```

Note that if the flask server is not running while making a ```curl``` request then you will get an error.
Now we will test the routes in ```iss_tracker.py```. An example of a route that will be tested is:
```
curl localhost:5000/epoch
```

### Example Outputs
Example output for ```/```:
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

Example output for ```/epoch```: 
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

Example output for ```/epoch/1```: 
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

Example output for ```/epoch/1/speed```:
```
speed: 7.662046317290625 km/s
```

