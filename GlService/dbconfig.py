from flask import Flask
from flask_mongoengine import MongoEngine
from mongoengine import connect
from mongoengine.connection import disconnect
app = Flask(__name__)
app.config['MONGODB_DB'] = 'generalledgerdb'
db = MongoEngine(app)
connect('db', host='localhost', port=27017, alias='generalledgerdb')