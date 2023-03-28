# Homework 06
## Objective
The purpose of this assignment is to practice software design including REST APIs (Representational State Transfer Application Programming Interfaces), the Flask Application, Redis, creating routes in Flask using type annotations and docstrings, working with complex JSON data, and containerization. 

## Contents
This folder includes 1 script, 1 Dockerfile, 1 docker-compose, and 1 README file.

## Required Modules
This project requires the installation of the requests, Flask, json, and redis modules. Install these modules with the ```pip install``` command in the command line.

## Gene Data
The Human Genome Organization (HUGO) oversees the HUGO Gene Nomenclature Committee (HGNC) who “approves a unique and meaningful name for every gene”. This project uses the complete set of HGNC data. This data includes information about the id, symbol, name, family, and more for each gene.

Find data archives on gene data at HGNC: https://www.genenames.org/download/archive/. 

### Part 1 - Routes
Below are app routes to navigate this API. The requests, json, and redis modules are used to turn the gene data into a usable dictionary. 

| Route | Method | What it should return | 
| ---------------------------- | ---------------------------- | ---------------------------- |
| ```/data``` | GET | return all data from redis |
| ```/data``` | POST |  put data into redis | 
| ```/data``` | DELETE | delete data in redis | 
| ```/genes``` | GET | return a list of all hgnc_ids |
| ```/genes/<hgnc_id>``` | GET | return all data associated with a specific hgnc_id |


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


## Instructions
### Pull the Image from Docker Hub
To get the image from Docker Hub use the command ```docker pull silvermadison/gene_api:1.0```.


### Build a New Image from This Dockerfile
In order to retrieve the data from this repository use the command
```
git clone git@github.com:silvermadison/my-coe332-hws.git
```
This will provide you with all the data in this repository. Navigate to the homework06 folder to access its contents so you can follow along with this project.

Create the image using the command ```docker build -t silvermadison/gene_api:1.0 .```.

Check to make sure the image is there using the command```docker images```. Output should look similar to:
```
REPOSITORY                  TAG       IMAGE ID       CREATED          SIZE
silvermadison/gene_api   1.0      9b88163e71e8   7 minutes ago    897MB
```

### Run the Containerized App
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
Quit the python interpreter with ```quit()```. Finally run redis and Flask using the docker compose file with the command ```docker-compose up```. 
With the container running, you can test the API with ```curl``` commands. In order to run the code, open another tab in your linux operating system so that you have two tabs total. In one tab the container is running in the foreground and in the other tab you are testing the API.
