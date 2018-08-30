from bson.objectid import ObjectId 

class Usuario:
	
	def __init__(self,_usuario=None,_password=None,_email=None):
		self._id = ObjectId()
		self.usuario = _usuario
		self.password = _password
		self.email = _email