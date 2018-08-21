# SO
import os

# WebApp
from flask import Flask
from webBP import webBP

# MongoDB
from Mongo import Mongo

PORT = 8443
HOST = "0.0.0.0"
MONGODB = "mongodb://atrpapa:atr123@ds219672.mlab.com:19672/autorenew"

app = Flask(__name__)

if __name__ == "__main__":
	
	mongo = Mongo(MONGODB)
	
	app.secret_key = os.urandom(12)
	app.register_blueprint(webBP)
	app.run(HOST,PORT)