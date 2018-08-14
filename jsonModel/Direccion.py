from bson.objectid import ObjectId 

class Direccion:

	def __init__(self,_nombre=None,_numero=None,_boolean=None):
		self.nombre = _nombre
		self.numero = _numero
		self.boolean = _boolean