import os
import imaplib
import email
from email.message import EmailMessage
import ssl
import smtplib
import random

imap_server = 'imap.gmail.com'
email_sender = 'josephkrol2002@gmail.com'
email_password = 'uqfrmyxstsfnmtkg'
email_receiver = 'josephkrol2002@gmail.com'
code = (str)(random.randint(1000000, 9999999))
adressenlijst = []
mailnummer_dubbel = []
dubbel = False


subject = 'stem'
body = "Beste stemmer, \nJouw persoonlijke code is: " + code + "\nGa naar https://josephs.io/ om je stem in te willigen. Veel succes."

imap = imaplib.IMAP4_SSL(imap_server)
imap.login(email_receiver, email_password)

imap.select("Inbox")
#imap.select("Spam")

_, msgnums = imap.search(None, 'subject "stem"')

# voor elke mail in inbox met onderwerp: stem
for msgnum in msgnums[0].split():
    _, data = imap.fetch(msgnum, "(RFC822)")
    message = email.message_from_bytes(data[0][1])

    zender = f"{message.get('From')}"
    #print(str(zender))
    
    #i = 0
    x = 0
    for x in range(len(adressenlijst)):
        if (adressenlijst[x] == str(zender)):
            dubbel = True
            break
    
    if (dubbel == False):
        email_receiver = zender

    adressenlijst.append(str(zender))
    #print(adressenlijst[x])
    # check dezelfde adressen.
    # verwijder herhalingen.
    # Doorzoek string op keyword uva.nl. als keyword niet in string, geen mail.

em = EmailMessage()
em['From'] = email_sender
em['To'] = email_receiver
em['Subject'] = subject
em.set_content(body)

context = ssl.create_default_context()

if "uva.nl" in email_receiver:
    uvamail = True
else:
    uvamail = False



with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
    smtp.login(email_sender, email_password)
    if (dubbel == False):
        if (uvamail == True):
            smtp.sendmail(email_sender, email_receiver, em.as_string())
            os.system("echo " + code + " >> codes.txt")
