from pymongo import MongoClient

class Mongo():
	
	instance = None
	
	def __new__(cls,_url=None):
		
		if(Mongo.instance == None):
			Mongo.instance = MongoClient(_url)
		return Mongo
	
	def getUsuarios():
		return Mongo.instance.autorenew.usuarios
		
	def getRegistros():
		return Mongo.instance.autorenew.registros