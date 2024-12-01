# My Flask Scheduling App Documentation
## Overview
This is a Python Flask app for managing MLOps deployments.

## Setup
1. Build the Docker image and deploy app 
 ```bash 
 docker-compose up
```
app runs @ 0.0.0.0:5001 
on the host device

2. This will build and deploy the flask application,
3. Redis: The compose file will pull redis for queue system
4. MongoDb: mongodb is used as the backend Db and will be pulled by compose file

## How does it work
1. flask server with below mentioned services gets deployed, where user can signup, login create and deploy jobs
2. A Daemon run in backgorund every 5 seconds watching the queue to schedule jobs which are in queue based on the availablity and capacity of clusters
    each job when scheduled have a priority, in redis implemented a priority queue, in which when a task is received, it is added to the queue based on the priority. and the daemon always tries to schedule the most priority job( ie priority 1). with the required resources for the it will search for any cluster with the given resources or more available then its gets scheduled. If not it will be queued back again.

## How to use:
Not able to implement test cases however. I will detail the apis and functionalities

1. to access the app hit : localhost:5001/
following are the apis and functionalities:
1. /signup
    curl --location 'localhost:5001/signup' \
        --header 'Content-Type: application/json' \
        --data '{
            "username" : "amish",
            "password" : "amish",
            "organization_id": "1"
        }'
    user with username and password will be created
2. /login
    curl --location 'localhost:5000/login' \
        --header 'Content-Type: application/json' \
        --data '{
            "username" : "amish",
            "password" : "amish",
            "organization_id": "1"
        }'
    response : <token>:<token>
    The mentioned user gets logged in. 
    Note : The response have jwt token <token>(this required for further apis). So copy the token use it for below apis
3. /clusters/create
    curl --location 'localhost:5000/clusters/create' \
        --header 'Authorization: Bearer <token>' \
        --header 'Content-Type: application/json' \
        --data '{
            "name" : "cluster1",
            "cpu" : 100,
            "ram" : 200,
            "gpu" : 200
        }'
    This will create a cluster : cluster1 with the above mentioned capacities/
    Note: replace the <token> with token received from /login api

4. /clusters
    curl --location '0.0.0.0:50001/clusters' \
        --header 'Authorization: Bearer <token>'
    This api will list out all cluster detailing max, available, used resources.

5. /deployments
    curl --location 'localhost:50001/deployments' \
    --header 'Authorization: Bearer <token>' \
    --header 'Content-Type: application/json' \
    --data '{
        "cluster_name" : "cluster1",
        "image_path" : "s3://a/bucket/with/some/image/present",
        "priority" : 20,
        "required_cpu" : 20,
        "required_ram" : 15,
        "required_gpu" : 8
    }'
    This api will deploy/queue the given job based on priority and availability of cluster

6. /deployments/queue
    curl --location --request GET 'localhost:50001/deployments/queue' \
    --header 'Authorization: Bearer <token>' \
    --header 'Content-Type: application/json' \
    --data '{
        "cluster_name" : "cluster1",
        "image_path" : "s3://abucket/with/some/image/present",
        "priority" : 20,
        "required_cpu" : 20,
        "required_ram" : 15,
        "required_gpu" : 8
    }'
    This will give the current queue with jobs waiting for deployements in order of the priority.

# Thank you for you valueble time to go through and/or evaluate the assignement.
