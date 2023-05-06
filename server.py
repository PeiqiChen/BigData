from flask import Flask, request, render_template, redirect, session, jsonify
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


    print("user")
    return render_template('success.html')

 # Define route for user login
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        # Get form data from request
        #data = request.get_json()
        # Find the user in the database
        user = users_collection.find_one({'username': request.form.get('username')})
        print("1111" + user['password'])
        if user and check_password_hash(user['password'], request.form.get('password')):
        # If login credentials are valid, store user_id in session
            session['id'] = str(user['_id'])
            print(str(user['_id']))
            return redirect('/dashboard')
        else:
            error_message = 'Invalid username or password. Please try again.'
            return render_template('login.html', error_message=error_message)
    else:
        return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    # Retrieve user ID from session
    user_id = session.get('id')
    if user_id:
        # If user is logged in, retrieve user profile from database and render dashboard
        user = users_collection.find_one({'_id': ObjectId(user_id)})
        jobs = recommend(user['tech_stack'])
        ##
        print(user)
        print(jobs)
        return render_template('dashboard.html', user=user, jobs = jobs)
    else:
        # If user is not logged in, redirect to login page
        return redirect('/login')

@app.route('/findall')
def findall():
    alluser =  users_collection.find()
    for u in alluser:
        print(u)
    return render_template('findall.html',users=alluser)

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('id', None)
    print("here")
    return redirect('/login')

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
