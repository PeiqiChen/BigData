from flask import Flask
import json
# from search import find_jobs_in_location_and_title
# from flask_mongoengine import MongoEngine
# from flask_login import LoginManager
# from user import db
# from routes import bp as routes_bp

app = Flask(__name__)
# app.register_blueprint(routes_bp)

@app.route("/users")
def users():
    return {"users": ["pc3082", "user2", "user3"]}

@app.route("/search/<role>/<location>")
def search(role, location="United States"):
    f = open('test.json')
    data = json.load(f)
    print(role)
    print(location)
    # list = find_jobs_in_location_and_title(role, location)
    # data = json.dumps(list)
    return data

if __name__ == "__main__":
    app.run(debug=True)