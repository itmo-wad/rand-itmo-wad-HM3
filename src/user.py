import bcrypt
from flask import session

from response import Response


class User:
    def __init__(self, config):
        self.name = None
        self.username = None
        self.collection = config.USERS_COLLECTION
        self.session_key = 'username'
        self.response = Response()

    def login(self, username, password):
        try:
            user = self.collection.find_one({'username': username})
            if user is None:
                self.response.add_error('User not found!...')
            else:
                if bcrypt.checkpw(password.encode('utf-8'), user['password']):
                    self.username = user['username']
                    self.response.data = {
                        'username': self.username
                    }
                else:
                    self.response.add_error('Credentials not correct! ...')

        except:
            self.response.add_error('error')

        return self.response

    def signup(self, name, username, password):
        if self.collection.find_one({"username": username}):
            self.response.add_error('Username already exists, try another one ...')
        else:
            password_hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            record = {'name': name, 'username': username, 'password': password_hashed}
            self.collection.insert_one(record)
            self.username = username
            self.response.data = {
                'username': self.username
            }
            self.response.message = 'User registered ...'

        return self.response

    def start_session(self, obj):
        session[self.session_key] = obj
        return True

    def logout(self):
        if session.pop(self.session_key, None):
            return True
        else:
            return False

    def get_user_id(self, username):
        user = self.collection.find_one({'username': username})
        if user is None:
            self.response.add_error('User not found! ...')
        else:
            self.response.data = {
                'id': user['_id'],
            }
        return self.response

    def get_user_by_id(self, id):
        user = self.collection.find_one({'_id': id})
        if user is None:
            self.response.add_error('User not found! ...')
        else:
            self.response.data = {
                'username': user['username'],
            }
        return self.response
