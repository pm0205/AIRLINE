

# import requests

import smtplib # use for sent email
import random # use for generate any random number
from email.mime.text import MIMEText # use for send email

# Import smtplib for the actual sending function

# Import the email modules we'll need
# from email.message import EmailMessage


class Sender():    
   
    def send_email(self,useremail):

        otp = random.randint(1000,9999) # generate otp

        server = smtplib.SMTP("smtp.gmail.com",587) #server name of gmail,port
        server.starttls() # use for security encryption
        sender_email = "amitnare4303@gmail.com" 
        sender_pass = "psgxoxgrucvnpyhe" # create password using app pass in manage gmail

        # emails = [ "1.gamil" , "2.gmail"]  use for send otp in multiple email
        receiver_email = useremail
        subject = f"Your otp code is {otp}"

        email_content = f"Hello {useremail},.. \nThis is message is from the AIRLINE-APP.\nFor security purpose, we have send an otp \n your OTP is {otp}. Please validate the otp in the app to validate your process." 
        # f use for merge sting and interger in one message

        msg = MIMEText(email_content)
        msg ["subject"] = subject
        msg ["from"] = sender_email
        msg ["to"] = receiver_email

        server.login(sender_email,sender_pass) # use for sender login 
        server.sendmail(sender_email, receiver_email, msg.as_string()) # use for sent mail
        server.quit() # sever exit
        print("otp sent done!") # confirmation message show you on terminal 

        return otp
    
# Sender().send_email('krithik.samal3@gmail.com')