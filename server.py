from flask import Flask, request, render_template, redirect, session, jsonify
import json
from flask_login import LoginManager
from user import User, users_collection, check_password_hash
import pymongo
import secrets
##from routes import bp as routes_bp
from bson.objectid import ObjectId
##from recommend import recommend

app = Flask(__name__)
##app.register_blueprint(routes_bp)
app.secret_key = secrets.token_hex(16)
##@app.route("/users")
##def users():
##    return {"users": ["pc3082", "user2", "user3"]}

@app.route("/search/<role>/<location>")
def search(role, location="United States", date_posted='any_time', remote_jobs_only = False, employment_type = "FULLTIME"):
    f = open('test.json')
    data = json.load(f)
    return data

@app.route('/register', methods= ['GET', 'POST'])
def register():
    if request.method == 'POST':

        # data = request.get_json()
        username =request.form.get('username')
        password = request.form.get('password')
        tech_stack = request.form.get('tech_stack')
        location = request.form.get('location')
        #user_id = users_collection.count_documents({}) + 1
        user = User(username=username, password=password, tech_stack=tech_stack, location=location)
        user.save() 
        return redirect('/success')

    return render_template('signup.html')

@app.route('/success', methods=['GET', 'POST'])
def success():

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
        ##jobs = recommend(user['tech_stack'])
        print(user)
        return render_template('dashboard.html', user=user)
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


if __name__ == "__main__":
    client = pymongo.MongoClient("mongodb://localhost:27017")
    db = client["bigdata"]
    collections = ["cloud_developer", "data_scientist", "researcher", "software_engineer", "technical_manager"]
    app.run(debug=True)