# Homework 08 - Gene API with Kubernetes and Images
## Objective
The purpose of this assignment is to practice software design including plotting data, Kubernetes, Redis, REST APIs (Representational State Transfer Application Programming Interfaces), the Flask Application, creating routes in Flask using type annotations and docstrings, working with complex JSON data, and containerization. 


## Contents
This folder includes 1 script, 1 Dockerfile, 1 docker-compose, 7 yaml files, and 1 README file. 


## Required Modules
This project requires the installation of the requests, Flask, json, redis, and matplotlib modules. Install these modules with the ```pip install``` command in the command line (note: an additional ```-- user``` is needed after install and before the module name for both requests and flask). This project also requires a console with Kubernetes access.


## Gene Data
The Human Genome Organization (HUGO) oversees the HUGO Gene Nomenclature Committee (HGNC) who “approves a unique and meaningful name for every gene”. This project uses the complete set of HGNC data. This data includes information about the id, symbol, name, family, and more for each gene.


Find data archives on gene data at HGNC: https://www.genenames.org/download/archive/. 


### Part 1 - Routes
Below are app routes to navigate this API. The requests, json, and redis modules are used to turn the gene data into a usable dictionary that is then stored in redis. 


| Route | Method | What it should return | 
| ---------------------------- | ---------------------------- | ---------------------------- |
| ```/data``` | GET | return all data from redis |
| ```/data``` | POST |  put data into redis | 
| ```/data``` | DELETE | delete data in redis | 
| ```/genes``` | GET | return a list of all hgnc_ids |
| ```/genes/<hgnc_id>``` | GET | return all data associated with a specific hgnc_id |
| ```/image``` | POST | read the gene group IDs and create a histogram image to be uploaded into the redis database |
| ```/image``` | GET | return the image to the user if it is in the database | 
| ```/image``` | DELETE | delete the image from the redis database |




### Part 2 - Dockerfile 
The Dockerfile contains commands for building a new image. When creating the Dockerfile the image should contain the same versions of modules as you are using on the Jetstream VM; this will be reflected in the ```FROM``` and ```RUN``` instructions. We will do this for the modules python, flask, and requests.


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

To check your version of matplotlib, in the VM command line run ```pip freeze | grep matplotlib```. Output should look similar to:
```
matplotlib==3.7.1
```
The version of matplotlib I am using is 3.7.1 and this version is also used in the ```RUN``` instruction in the Dockerfile.




## Instructions
### Pull the Image from Docker Hub
To get the image from Docker Hub use the command ```docker pull silvermadison/gene_api:1.0```.




### Build a New Image from This Dockerfile
In order to retrieve the data from this repository use the command
```
git clone git@github.com:silvermadison/my-coe332-hws.git
```
This will provide you with all the data in this repository. Navigate to the homework08 folder to access its contents so you can follow along with this project.


Create the image using the command ```docker build -t silvermadison/gene_api:1.0 .```.


Check to make sure the image is there using the command ```docker images```. Output should look similar to:
```
REPOSITORY                  TAG       IMAGE ID       CREATED          SIZE
silvermadison/gene_api   1.0      9b88163e71e8   7 minutes ago    897MB
```


### Kubernetes
All the yaml files in the repository need to be created and uploaded to Kubernetes. Do so through the command ```kubectl apply -f <filename>``` on the Kubernetes accessible machine. After each command line you should get a statement saying the file was created. 
Ensure the files are running properly. For the command ```kubectl get pods``` output should look like:
```
NAME                                    READY   STATUS    RESTARTS        AGE
msilver-test-flask-6568f5856d-k2mxd     1/1     Running   0               2h
msilver-test-redis-758b75b5c8-cnkcz     1/1     Running   0               3h
py-debug-deployment-f484b4b99-wxdsx     1/1     Running   0               8d
```
And, for the command ```kubectl get services``` output should look similar to:
```
NAME                 TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)    AGE
msilver-test-flask   ClusterIP   10.233.35.77    <none>        5000/TCP   36h
``` 


### Accessing the API
After running the ```kubectl get pods``` command, notice the python debug deployment pod. In order to make commands on the API, we will need to run a shell in this pod. Do so with: ```kubectl exec -it <python debug deployment pod name> – /bin/bash```.
The shell prompt should change to the following, which shows that you are “inside” the container: ```root@py-debug-deployment-f484b4b99-wxdsx:/#```. From here, run an API route. Note the Cluster-IP address for your service after the command  ```kubectl get services```. This IP will be used in replacement for “localhost”.

### API Command Examples
The ```/data``` and ```/image``` routes include three different methods (POST, GET, DELETE). To specify which method use the notation ```-X <METHOD>``` after the curl command. If no method is specified, it is assumed to be a “GET” method. The ```/data``` will complete one of the three tasks based on the method given: **post** the data to Redis, return/**get** the data for the user, or **delete** the data from the Redis database. The ```/image``` will complete one of the three tasks based on the method given: **post** the image to Redis which is a histogram of the number of gene group ID numbers in the databse, return/**get** the image to the user, or **delete** the image from the Redis database.
An example: ```curl -X DELETE 10.233.35.77:5000/data```
```
data deleted, there are 0 keys in the database
```
The ```/genes``` route returns a list of all the HGNC genes in the Redis database. Use the command: ```curl 10.233.35.77:5000/genes```.

The ```/genes/<hgnc_id>``` route returns all the information associated with a given <hgnc_id> that is within the Redis database. Use the command: ```curl 10.233.35.77:5000/genes/HGNC:9987```.

