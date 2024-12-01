import redis
from app.models import Deployment, Cluster
from time import sleep
from app import mongo
from bson import ObjectId

redis_client = redis.StrictRedis.from_url("redis://redis:6379/0")

def schedule_deployments():
    while True:
        # Try to get the first deployment from the queue
        deployment_data = redis_client.zpopmin('deployment_queue')
        print("deployment_data : ", deployment_data)
        if len(deployment_data)==0:
            print("no deplyment found ")
            sleep(5)
            continue
        deployment_id = deployment_data[0][0].decode('utf-8')
        print("deployment_id : ", str(deployment_id), type(deployment_id))
        if deployment_id:
            deployment = mongo.db.deployments.find_one({"_id": ObjectId(deployment_id)})
            print("Scheduler : ", deployment['cluster_name'], type(deployment['required_cpu']), deployment['required_ram'], deployment['required_gpu'])
            query = {
                "available_resources.cpu": {"$gte": int(deployment['required_cpu'])},
                "available_resources.ram": {"$gte": int(deployment['required_ram'])},
                "available_resources.gpu": {"$gte": int(deployment['required_gpu'])}
            }
            cluster = mongo.db.clusters.find_one(query)
            print("cluster : ", cluster)
            if cluster : 
                # Allocate resources
                mongo.db.clusters.update_one(
                    {"_id": cluster['_id']},
                    {"$inc": {"allocated_resources.cpu": deployment['required_cpu'],
                              "allocated_resources.ram": deployment['required_ram'],
                              "allocated_resources.gpu": deployment['required_gpu'],

                              "available_resources.cpu": -deployment['required_cpu'],
                              "available_resources.ram": -deployment['required_ram'],
                              "available_resources.gpu": -deployment['required_gpu']
                              }}
                )

                # Update deployment status
                mongo.db.deployments.update_one(
                    {"_id": deployment['_id']},
                    {"$set": {"status": "running"}}
                )
                print(f"Deployment {deployment['_id']} started.")
                
            else:
                # Re-queue deployment if not enough resources
                # redis_client.zadd('deployment_queue', {deployment_id)
                push_to_queue({deployment_data[0][0]:deployment_data[0][1]})
                print(f"Not enough resources for deployment {deployment['_id']}. Re-queued.")
        
        sleep(5)

def push_to_queue(data= {}):
    '''function to optimise the queue and reschedule the queue'''

    if len(data) != 0:
        # get the entire queue
        # reque it based on priority: ie add this element to priority queue
        print("push_tot_queue : ", data)
        redis_client.zadd('deployment_queue',data)
