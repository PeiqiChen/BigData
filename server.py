from flask import Flask
import json
# from search_filters import search_jobs
import pymongo
import datetime
import pandas as pd
# from flask_mongoengine import MongoEngine
# from flask_login import LoginManager
# from user import db
# from routes import bp as routes_bp

def search_jobs(job_title=None, location=None, date_posted=None, remote_jobs_only=None, employment_type=None):
    query = {}
    if job_title:
        query["job_title"] = {"$regex": job_title, "$options": "i"} # Use a case-insensitive regex for partial matching
    if location:
        query["$or"] = [{"job_city": {"$regex": location, "$options": "i"}},
                        {"job_state": {"$regex": location, "$options": "i"}},
                        {"job_country": {"$regex": location, "$options": "i"}}]
    if date_posted:
        current_time = datetime.datetime.now()
        if date_posted == "past_24_hours":
            time_threshold = current_time - datetime.timedelta(days=1)
        elif date_posted == "past_week":
            time_threshold = current_time - datetime.timedelta(weeks=1)
        elif date_posted == "past_month":
            time_threshold = current_time - datetime.timedelta(weeks=4)
        else:  # Default to any time
            time_threshold = None
        if time_threshold:
            query["job_posted_at_datetime_utc"] = {"$gte": time_threshold.isoformat()}
    if remote_jobs_only:
        query["job_is_remote"] = True
    if employment_type:
        query["job_employment_type"] = {"$regex": employment_type, "$options": "i"}

    matching_jobs = []
    
    for collection_name in collections:
        collection = db[collection_name]
        for job in collection.find(query):
            matching_jobs.append(job)
    # Create a pandas DataFrame from the job data
    df = pd.DataFrame(matching_jobs)
    # Save the DataFrame to an Excel file
    df.to_excel('result.xlsx', index=False)
    return matching_jobs





app = Flask(__name__)
# app.register_blueprint(routes_bp)

@app.route("/users")
def users():
    return {"users": ["pc3082", "user2", "user3"]}

@app.route("/search/<role>/<location>/<date>/<remote>/<type>")
def search(role, location="United States", date='any_time', remote = False, type = "FULLTIME"):
    f = open('data/cloud_developer.json')#test.json')
    data = json.load(f)
    # list = search_jobs(role, location, date_posted, remote_jobs_only, employment_type)
    # data = json.dumps(list)
    # print(data)
    return data

if __name__ == "__main__":
    client = pymongo.MongoClient("mongodb://localhost:27017")
    db = client["bigdata"]
    collections = ["cloud_developer", "data_scientist", "researcher", "software_engineer", "technical_manager"]
    app.run(debug=True)