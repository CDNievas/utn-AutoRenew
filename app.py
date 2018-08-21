# SO
import os

# WebApp
from flask import Flask
from webBP import webBP

# MongoDB
from Mongo import Mongo

PORT = os.environ.get("PORT")
HOST = "utn-autorenew.herokuapp.com"
MONGODB = os.environ.get("MONGODB")

app = Flask(__name__)

if __name__ == "__main__":
	
	mongo = Mongo(MONGODB)
	
	app.secret_key = os.urandom(12)
	app.register_blueprint(webBP)
	app.run(HOST,PORT)