from bs4 import BeautifulSoup
import requests
import json

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
		return False
	else :
		return True
	
	"""
	
		tag = parser.find("form")
		postWeb = tag.get("action")
		
		tag = parser.find("input",{"name":"SAMLResponse"})
		samlResponse = tag.get("value")	
		
		tag = parser.find("input",{"name":"RelayState"})
		relayState = tag.get("value")		
		
		payload = {"SAMLResponse":samlResponse,
			       "RelayState":relayState}
		
		r = session.post(postWeb,headers=headers,data=payload)
		
		print(r.text)"""