from flask import Flask
import json
from search_filters import search_jobs
from recommend import recommend
import pymongo
import pandas as pd
from bson.json_util import dumps
import secrets



app = Flask(__name__)
app.secret_key = secrets.token_hex(16)


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

@app.route("/recommend/<username>/<userinfo>")
def recommend_job(username, userinfo):
    # f = open('data/cloud_developer.json')#test.json')
    # data = json.load(f)
    # print(username, userinfo)
    ##
    document = collection.find_one(sort=[("_id", pymongo.DESCENDING)])
    tech_stack = document['bigdata']['user'].get('tech_stack', '')
    location = document['bigdata']['user'].get('location', '')
    jobs_for_looking = document['bigdata']['user'].get('jobs_for_looking', '')
    userinfo=jobs_for_looking+location+tech_stack

    '''["User Experience Researcher", "Greenhouse", "1Vq_lpiZB_wAAAAAAAAAAA==",
    "Intrinsic", 1676937600, "FULLTIME",
    "Researcher", "Mountain View", "CA"], '''
    list = recommend(userinfo)
    keys = ['job_title','job_publisher','job_id',
            'employer_name','job_posted_at_timestamp','job_employment_type',
            'job_job_title', 'job_city','job_state']
    data_map = []
    list = list.replace("\"","")
    list = list.replace("[[","")
    list = list.replace("]]","")
    for l in list.split("], ["):
        # print(l)
        ele = l.split(", ")
        tmp = {}
        idx = 0
        for idx in range(0,len(ele)):
            # print(ele)
            if ele[idx] == 'null':
                tmp[keys[idx]] = ''
            else:
                tmp[keys[idx]] = ele[idx]
            idx += 1

        data_map.append(tmp)
    data = json.dumps(data_map)
    # print(data)
    return data


if __name__ == "__main__":
    client = pymongo.MongoClient("mongodb://localhost:27017")
    db = client["bigdata"]
    collections = ["cloud_developer", "data_scientist", "researcher", "software_engineer", "technical_manager"]
    usercollect=['users']
    app.run(debug=True)
