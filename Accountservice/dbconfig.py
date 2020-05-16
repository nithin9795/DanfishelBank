from flask import Flask
from flask_mongoengine import MongoEngine
from mongoengine import connect

app = Flask(__name__)
app.config['MONGODB_DB'] = 'savingaccount_service'
db = MongoEngine(app)
connect('db', host='localhost', port=27017, alias='savingaccountdb')