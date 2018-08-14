from jsonModel import *
from jsonModel import __classes__

from pymongo import *

from bson.objectid import ObjectId 
from functools import reduce
import json,sys

def jsonToObj(anDict):
	
	if(anDict == None):
		return None
	
	strClass = anDict["__class__"]
	aClass = strToClass(strClass)
	anObj = aClass()
	
	for key in anDict:
		
		if(key != "__class__"):
			
			value = anDict[key]
			try:
				
				if isinstance(value,list):
											
					listValue = []
					for jsonObjList in value:
						listValue.append(jsonToObj(jsonObjList))
					value = listValue				
				
				elif isinstance(value,dict):
					value = jsonToObj(value)
					
				setattr(anObj,key,value)				
			
			except AttributeError:
				print(aClass.__name__ + " doesn't have attribute " + key)
			
	return anObj

def objToJson(obj):

	objJson = dict()
	objJson["__class__"] = classToStr(obj)
	
	for attr, value in obj.__dict__.items():
		
		
		if isinstance(value,(int,bool,float,str)):
			objJson[attr] = value
			
		# Converts list	
		elif isinstance(value,list):
			jsonList = []
			for objList in value:
				objJsonList = objToJson(objList)
				jsonList.append(objJsonList)				
			objJson[attr] = jsonList
		
		elif value is None:
			objJson[attr] = None
		
		elif isinstance(value, ObjectId):
			objJson[attr] = str(ObjectId(value))
			
		# Next iteration
		elif isinstance(value,set):
			raise TypeError("Doesn't support sets, convert it to a list")
		
		# Next iteration
		elif isinstance(value,tuple):
			raise TypeError("Doesn't support tuples, convert it to an object")
		
		# Next iteration
		elif isinstance(value,dict):
			raise TypeError("Doesn't support dictionaries, convert it to an object")
		
		# Is user defined object
		else:
			objJson[attr] = objToJson(value)
			
	return objJson

def updateInto(obj,db):
	db.replace_one({"_id":str(obj._id)},objToJson(obj))

def insertInto(obj,db):
	db.insert_one(objToJson(obj))


# Auxiliar functions

def classToStr(obj):
	return searchByValue(type(obj))

def strToClass(idClass):
	try:
		return __classes__[idClass]
	except KeyError:
		raise KeyError("ID: " + str(idClass) + " not defined in __classes__ at __init.py__")

def searchByValue(aValue):
	for key, value in __classes__.items():
		if value == aValue:
			return key
	raise KeyError("Class: " + str(aValue) + " not defined in __classes__ at __init.py__")