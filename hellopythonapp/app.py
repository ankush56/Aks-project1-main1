import os
import pymongo
from pymongo import MongoClient
from flask import Flask, render_template, request
app = Flask(__name__)

#######################################################
# This section writes hello world on persistent volume mounted to containers
#Persistent storage use
# Get the path of the PV from an environment variable
# set DATA_PATH env var as path to which pvc is mounted
data_path = os.environ.get('DATA_PATH', '/app/appdata')

admin1 = os.environ.get('MONGO_USERNAME')
pass1 = os.environ.get('MONGO_PASSWORD')

environment = os.environ.get('environment')

# Use the data_path to read and write data
with open(f'{data_path}/mydata.txt', 'w') as f:
    f.write('Hello, World!')

with open(f'{data_path}/myenv.txt', 'w') as f:
    f.write(environment)    

with open(f'{data_path}/mydata.txt', 'r') as f:
    print(f.read())

#########################################################
############ MongoDB Read and Write #####################
@app.route("/add", methods=["POST"])
def add():
    name = request.form["name"]
    age = request.form["age"]
    # Connect to MongoDB
    #client = pymongo.MongoClient("mongodb://mongodb:27017/")
    # client = pymongo.MongoClient(f"mongodb://{MONGO_INITDB_ROOT_USERNAME}:{MONGO_INITDB_ROOT_PASSWORD}@mongodb:27017/")
    client = pymongo.MongoClient(f"mongodb://{admin1}:{pass1}@mongodb:27017/")
    db = client["mydatabase"]
    collection = db["test_collection"]
    data = {"name": name, "age": age}
    collection.insert_one(data)
    return "Successfully added to the database!"

@app.route("/showdata")
def showdata():
    # Connect to MongoDB
    #client = pymongo.MongoClient("mongodb://mongodb:27017/")
    #client = pymongo.MongoClient(f"mongodb://{MONGO_INITDB_ROOT_USERNAME}:{MONGO_INITDB_ROOT_PASSWORD}@mongodb:27017/")
    client = pymongo.MongoClient(f"mongodb://{admin1}:{pass1}@mongodb:27017/")
    db = client["mydatabase"]
    collection = db["test_collection"]
    # Query all data from the collection
    results = collection.find({})
    return render_template('showdata.html', results=results)    


####################################################
@app.route("/")
def hello():
    return render_template('index.html', message=environment)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)