#OS
import time

# Web
from flask import Blueprint, request, render_template, flash

from botRenew import *

# MongoDB
from Mongo import *
import Koala
from jsonModel import *

from emailSend import *

webBP = Blueprint("webBP", __name__, template_folder="webfiles")

@webBP.route("/")
def home():
	users = Mongo.getUsuarios().count()
	libros = Mongo.getRegistros().count()
	return render_template("home.html", users=users, libros=libros)

@webBP.route("/renew")
def renew():
	print("Starting AutoRenew - " + time.ctime())
	usuarios = Mongo.getUsuarios()	
	usuarios = usuarios.find({})
	
	for usuario in usuarios:
		renewLibros(usuario["usuario"],usuario["password"])
	
	cantUsers = usuarios.count()
	print("Usuarios renovados: {}".format(cantUsers))	
	
	return "OK"

@webBP.route("/jaja")
def asdasd():
	print("Enviando email - " + time.ctime())
	enviarEmail("cdnievas@hotmail.com")
	return "OK"

@webBP.route("/doPost", methods=["POST"])
def doPost():
	user = request.form["username"]
	password =  request.form["password"]
	email = request.form["email"]
	
	if(campoVacio(user) or campoVacio(password) or campoVacio(email)):
		
		flash("Algun campo se encontraba vacio", "error")
	
	else:
		
		if userExists(user,password):
		
			if "register" in request.form:
				
				nro = register(user, password, email)
				
				if nro == 1:
					flash("El usuario ya se encuentra en el sistema", "error")
				else:
					flash("Se ha registrado al usuario correctamente", "success")
					
			else:
				
				nro = delete(user, password, email)
				
				if nro == 1:
					flash("El usuario no se encuentra en el sistema", "error")
				else:
					flash("Se ha borrado al usuario correctamente", "success")			
				
		else:
			flash("Usuario/Contraseña incorrecta", "error")		

	return home()

def register(user,password,email):
	
	usuarios = Mongo().getUsuarios()
	match = usuarios.find({"usuario":user,"password":password}).count()
	
	if match == 0:	
		usuario = Usuario(user,password,email)
		Koala.insertInto(usuario,usuarios)
		renewLibros(user,password,email)
		return 0
	else:
		return 1
 
def delete(user,password,email):
	
	usuarios = Mongo().getUsuarios()
	match = usuarios.find({"usuario":user,"password":password}).count()
	
	if match == 1:
		usuarios.remove({"usuario":user,"password":password})
		return 0
	else:
		return 1

def campoVacio(campo):
	return not(bool(str(campo))) or str(campo) == "" or not(bool(str(campo).split()))

