from bson.objectid import ObjectId 

class Registro:
	
	def __init__(self,_usuario=None,_libroId=None,_time=None):
		self._id = ObjectId()
		self.usuario = _usuario
		self.libroId = _libroId
		self.time = _time