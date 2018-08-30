#OS
import os

# Sendgrid
import sendgrid
from sendgrid.helpers.mail import *

def enviarEmail(email):
	
	sg = sendgrid.SendGridAPIClient(apikey=os.environ.get("SENDGRID_API_KEY"))
	from_email = Email("cdnievas@hotmail.com")
	subject = "UTN-AutoRenew -- Fallo la renovacion de su libro"
	to_email = Email(email)
	content = Content("text/plain", "La renovacion automatica de su libro fallo. Por favor chequeelo manualmente ingresando al sistema de la biblioteca")
	mail = Mail(from_email,subject,to_email,content)
	response = sg.client.mail.send.post(request_body=mail.get())