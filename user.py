from flask_login import UserMixin
from flask_mongoengine import MongoEngine
from werkzeug.security import generate_password_hash, check_password_hash
import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["bigdata"]
users_collection = db['users']  # Replace with your own collection name




class User(UserMixin):
    def __init__(self, id, username, password, tech_stack, location):
        self.id = id
        self.username = username
        self.password_hash = generate_password_hash(password)
        self.tech_stack = tech_stack
        self.location = location

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    @staticmethod
    def get(user_id):
        # Replace with your own logic to retrieve user from database
        user_data = users_collection.find_one({'id': user_id})
        if user_data:
            user = User(id=user_data['id'], username = user_data['username'], password=user_data['password'],
                        tech_stack=user_data['tech_stack'], location=user_data['location'])
            return user
        else:
            return None
        
    def save(self):
        # Convert user object to dictionary
        user_data = {
            'id': self.id,
            'username': self.username,
            'password': self.password_hash,
            'tech_stack': self.tech_stack,
            'location': self.location
        }

        # Insert user data into MongoDB
        users_collection.insert_one(user_data)
    

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False