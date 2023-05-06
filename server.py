from flask import Flask, request, render_template, redirect, session, jsonify
import json
from flask_login import LoginManager
from user import User, users_collection, check_password_hash
import pymongo
import secrets
##from routes import bp as routes_bp
from bson.objectid import ObjectId
from recommend import recommend

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

@app.route('/register', methods= ['GET', 'POST'])
def register():
    if request.method == 'POST':
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
