from flask import Flask
import json
from search_filters import search_jobs
import pymongo
import datetime
import pandas as pd
from bson.json_util import dumps
# from flask_mongoengine import MongoEngine
# from flask_login import LoginManager
# from user import db
# from routes import bp as routes_bp



app = Flask(__name__)
# app.register_blueprint(routes_bp)

@app.route("/users")
def users():
    return {"users": ["pc3082", "user2", "user3"]}

@app.route("/search/<role>/<location>/<date>/<remote>/<type>")
def search(role, location, date, remote, type):
    # f = open('data/cloud_developer.json')#test.json')
    # data = json.load(f)
    if remote=="false":
        remote = 'n'
    else:
        remote = 'y'
    list = search_jobs(role, location, date, remote, type)
    # print(len(list))
    if(len(list) == 0):
        f = open('data/cloud_developer.json')#test.json')
        data = json.load(f)
    else:
        tmp = dumps(list)
        json_data = json.loads(tmp)
        data = {}
        data['data'] = json_data
        data = json.dumps(data)  
        
    return data

if __name__ == "__main__":
    client = pymongo.MongoClient("mongodb://localhost:27017")
    db = client["bigdata"]
    collections = ["cloud_developer", "data_scientist", "researcher", "software_engineer", "technical_manager"]
    app.run(debug=True)