from flask import Blueprint, request, render_template, flash

from botRenew import *

# MongoDB
from Mongo import *
import Koala
from jsonModel import *

webBP = Blueprint("webBP", __name__, template_folder="webfiles")

@webBP.route("/")
def home():
	users = Mongo.getUsuarios().count()
	libros = Mongo.getRegistros().count()
	return render_template("home.html", users=users, libros=libros)

@webBP.route("/doPost", methods=["POST"])
def doPost():
	user = request.form["username"]
	password =  request.form["password"]
	
	if(campoVacio(user) or campoVacio(password)):
		
		flash("Algun campo se encontraba vacio", "error")
	
	else:
		
		if userExists(user,password):
		
			if "register" in request.form:
				
				nro = register(user, password)
				
				if nro == 1:
					flash("El usuario ya se encuentra en el sistema", "error")
				else:
					flash("Se ha registrado al usuario correctamente", "success")
					
			else:
				
				nro = delete(user, password)
				
				if nro == 1:
					flash("El usuario no se encuentra en el sistema", "error")
				else:
					flash("Se ha borrado al usuario correctamente", "success")			
				
		else:
			flash("Usuario/Contraseña incorrecta", "error")		

	return home()

def register(user,password):
	
	usuarios = Mongo().getUsuarios()
	match = usuarios.find({"usuario":user,"password":password}).count()
	
	if match == 0:	
		usuario = Usuario(user,password)
		Koala.insertInto(usuario,usuarios)
		renewLibros(user,password)
		return 0
	else:
		return 1
 
def delete(user,password):
	
	usuarios = Mongo().getUsuarios()
	match = usuarios.find({"usuario":user,"password":password}).count()
	
	if match == 1:
		usuarios.remove({"usuario":user,"password":password})
		return 0
	else:
		return 1

def campoVacio(campo):
	return not(bool(str(campo))) or str(campo) == "" or not(bool(str(campo).split()))
