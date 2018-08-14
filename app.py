# SO
import os, time
from threading import Thread

# WebApp
from flask import Flask
from webBP import webBP

from auxiliar import *

# MongoDB
from Mongo import Mongo

PORT = 8443
HOST = "0.0.0.0"
MONGODB = ""

app = Flask(__name__)

def autorenew():
	while(1):
		print("Starting AutoRenew - " + time.ctime())
		renewAll()
		time.sleep(30)
		
def renewAll():
	mongo = Mongo()
	usuarios = mongo.getUsuarios()	
	usuarios = usuarios.find({})
	
	for usuario in usuarios:
		renewLibros(usuario["usuario"],usuario["password"])
	
	cantUsers = usuarios.count()
	print("Usuarios renovados: {}".format(cantUsers))
	
if __name__ == "__main__":
	
	mongo = Mongo(MONGODB)
	
	thread = Thread(target=autorenew)
	thread.start()
	
	app.secret_key = os.urandom(12)
	app.register_blueprint(webBP)
	app.run(HOST,PORT)