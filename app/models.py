from app import mongo

class User:
    def __init__(self, username, password_hash, organization_id, role):
        self.username = username
        self.password_hash = password_hash
        self.organization_id = organization_id
        self.role = role

class Organization:
    def __init__(self, name, invite_code):
        self.name = name
        self.invite_code = invite_code

class Cluster:
    def __init__(self, name, cpu, ram, gpu):
        self.name = name
        self.cpu = cpu
        self.ram = ram
        self.gpu = gpu
        self.available_resources = {"cpu": cpu, "ram": ram, "gpu": gpu}
        self.allocated_resources = {"cpu": 0, "ram": 0, "gpu": 0}

    def create_cluster(self):
        cluster_data = {
            "name": self.name,
            "cpu": self.cpu,
            "ram": self.ram,
            "gpu": self.gpu,
            "available_resources": self.available_resources,
            "allocated_resources": self.allocated_resources
        }
        cluster_collection = mongo.db.clusters
        cluster_collection.insert_one(cluster_data)

class Deployment:
    def __init__(self, user_id, cluster_name, image_path, priority, required_cpu, required_ram, required_gpu):
        self.user_id = user_id
        self.cluster_name = cluster_name
        self.image_path = image_path
        self.priority = priority
        self.required_cpu = required_cpu
        self.required_ram = required_ram
        self.required_gpu = required_gpu
        self.status = "queued"

    def create_deployment(self):
        deployment_data = {
            "user_id": self.user_id,
            "cluster_name": self.cluster_name,
            "image_path": self.image_path,
            "priority": self.priority,
            "required_cpu": self.required_cpu,
            "required_ram": self.required_ram,
            "required_gpu": self.required_gpu,
            "status": self.status
        }
        deployment_collection = mongo.db.deployments
        deploy_data = deployment_collection.insert_one(deployment_data)
        print("deploy_data : ", deploy_data.inserted_id)
        return deploy_data.inserted_id
