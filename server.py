from flask import Flask
import json

app = Flask(__name__)

@app.route("/users")
def users():
    return {"users": ["pc3082", "user2", "user3"]}

@app.route("/search/<role>/<location>")
def search(role, location="United States"):
    f = open('test.json')
    data = json.load(f)
    print(role)
    print(location)
    return data
if __name__ == "__main__":
    app.run(debug=True)