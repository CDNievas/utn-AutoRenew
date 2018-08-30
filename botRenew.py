from bs4 import BeautifulSoup
import requests, json, re
from datetime import datetime

# MongoDB
from Mongo import *
import Koala
from jsonModel import *

def renewLibros(username,password):
	
	formArgs = obtenerFormulario()	
	session, request = login(formArgs,username,password)
	
	headers = {"Connection":"keep-alive",
	           "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"}	
	web = "https://biblioteca.frba.utn.edu.ar/opac_ver_prestamo.php"
	request = session.get(web, headers=headers, allow_redirects=True)
	
	parser = BeautifulSoup(request.text, "lxml")
	tags = parser.findAll("a",{"href":"javascript:;"})	

	if tags is not None:
		for tag in tags:			
			values = re.findall("\w+",tag.get("onclick"))

			prestamoId = values[1]
			ejemplarId = values[2]

			headers = {"Connection":"keep-alive",
			           "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"}	
			web = "https://biblioteca.frba.utn.edu.ar/ajax_renovar_prestamo.php"			

			payload = {"prestamoid":prestamoId,
			           "ejemplarid":ejemplarId}

			r = session.post(web,headers=headers,data=payload)

			""" Ejemplo de exito
			<h1 class = 'Titulo'><b>El Proceso de Renovaci&oacute;n fue realizado con &eacute;xito!</b></h1><span class='Texto'>
                            Por favor, tenga en cuenta que cada vez que se renueva un prestamo,
                            <br>se trata al mismo como <b>un prestamo nuevo</b>
                          </span><hr>
			"""

			# Renovacion hecha
			if "&eacute;xito" in r.text:
				reg = Registro(username,ejemplarId,str(datetime.now()))
				registros = Mongo().getRegistros()
				Koala.insertInto(reg,registros)
				
	print("Renove libros: {}".format(username))
				
				
def obtenerFormulario():
	
	headers = {"Connection":"keep-alive",
	           "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"}	
	web = "https://biblioteca.frba.utn.edu.ar/opac_principal.php"
	r = requests.get(web, headers=headers, allow_redirects=True)

	if r.history:
		# Maneja redireccion
		for resp in r.history:
			r = resp
			
	link = r.headers["Location"]
	session = requests.Session()
	r = session.get(link)

	parser = BeautifulSoup(r.text, "lxml")
	
	tag = parser.find("input",{"name":"AuthState"})
	authState = tag.get("value")
	
	postWeb = link + "/?"
	return (postWeb,authState,session)
	

def login(formArgs,username,password):	
	postWeb, authState, session = formArgs
	
	payload = {"username":username,
	        "password":password,
	        "AuthState":authState}
	
	headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
	           "Connection":"keep-alive"}	
	
	r = session.post(postWeb,headers=headers,data=payload)
	
	parser = BeautifulSoup(r.text, "lxml")
	
	tag=parser.find("div",{"class":"alert alert-danger"})
	
	if tag is not None:
		raise ValueError("Usuario inexistente")

	tag = parser.find("form")
	postWeb = tag.get("action")
	
	tag = parser.find("input",{"name":"SAMLResponse"})
	samlResponse = tag.get("value")	
	
	tag = parser.find("input",{"name":"RelayState"})
	relayState = tag.get("value")		
	
	payload = {"SAMLResponse":samlResponse,
		       "RelayState":relayState}
	
	r = session.post(postWeb,headers=headers,data=payload)
	
	return(session,r)

def userExists(user,password):
	formArgs = obtenerFormulario()	
	try:
		login(formArgs,user,password)
		return True
	except ValueError:
		return False