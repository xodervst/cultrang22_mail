from email.message import Message
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email import encoders
from string import Template
from fileinput import filename

from pathlib import Path
from pydoc import plain

import smtplib
import ssl
import csv


template=Template(Path("template.html").read_text())

#-----------------------------------------------------------
pdfname = 'Rulebook.pdf'
pdfname2 = 'PR_Broucher.pdf'

# open the file in bynary
binary_pdf = open(pdfname, 'rb')
binary_pdf2 = open(pdfname2, 'rb')

payload = MIMEBase('application', 'octate-stream', Name=pdfname)
payload.set_payload((binary_pdf).read())

payload2 = MIMEBase('application', 'octate-stream', Name=pdfname2)
payload2.set_payload((binary_pdf2).read())

# enconding the binary into base64
encoders.encode_base64(payload)
encoders.encode_base64(payload2)



# add header with pdf name
payload.add_header('Content-Decomposition', 'attachment', filename=pdfname)

payload2.add_header('Content-Decomposition', 'attachment', filename=pdfname2)


with open("mailer.csv") as file:  #Update the name of CSV file.
    r=csv.reader(file)
    list2=list(r)
    i=1
    for mail in list2:
        message=MIMEMultipart()
        message["from"]="Cultrang IIT Goa"   #This will be the name of the sender shown.
        message["to"]=mail[0]

        message["Subject"]="Invitation for IIT Goa's Cultural Festival, CultRang'22"  #Subject of the Email

        body=template.substitute({"name":"Nothing"})   #If the template recieves any substitute element, we can use this to send personalised mail.
        message.attach(MIMEText(body,"html"))
        # message.attach(MIMEImage(Path("Poster.png").read_bytes(),Name="Poster"))
        # message.attach(MIMEImage(Path("Talk1.png").read_bytes(),Name="Talk1"))
        # message.attach(MIMEImage(Path("Talk2.png").read_bytes(),Name="Talk2"))
        message.attach(payload)
        message.attach(payload2)


        with smtplib.SMTP(host="smtp.gmail.com",port=587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.login(user="#############",password="##########")  #Enter Your email id and Password
            smtp.send_message(message)
            print("Sent...",i,mail[0])
        i=i+1
    
