# OS
import time

# MongoDB
from app import MONGODB
from Mongo import Mongo

# Bot
from botRenew import renewLibros

# Scheduler
from apscheduler.schedulers.blocking import BlockingScheduler

# Worker
from worker import conn

q = Queue(connection=conn)
sched = BlockingScheduler()

@sched.scheduled_job("interval", minutes=1)
def autorenew():
	print("Starting AutoRenew - " + time.ctime())
	q.enqueue(renewAll)

def renewAll():
	mongo = Mongo(MONGODB)
	usuarios = mongo.getUsuarios()	
	usuarios = usuarios.find({})
	
	for usuario in usuarios:
		renewLibros(usuario["usuario"],usuario["password"])
	
	cantUsers = usuarios.count()
	print("Usuarios renovados: {}".format(cantUsers))

renewAll()
sched.start()
