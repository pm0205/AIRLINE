from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivymd.uix.screenmanager import ScreenManager
from kivymd.uix.screen import MDScreen
from kivy.core.text import LabelBase
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFloatingActionButton
from kivymd.uix.floatlayout import MDFloatLayout

from kivymd.uix.responsivelayout import MDResponsiveLayout # use for responsive
from kivymd.uix.list import OneLineAvatarIconListItem

import smtplib # use for sent email
import random # use for generate any random number
from email.mime.text import MIMEText # use for send email
# Import smtplib for the actual sending function
# Import the email modules we'll need
# from email.message import EmailMessage

class slope(MDApp):
    def build (self):
            
             screen_manager = ScreenManager()

             screen_manager.add_widget(Builder.load_file('sign-in.kv'))
             screen_manager.add_widget(Builder.load_file('sign-up.kv'))

             return screen_manager
        
   
    def send_email(self,user_email):

        useremail = user_email.text
        otp = random.randint(1000,9999) # generate otp

        server = smtplib.SMTP("smtp.gmail.com",587) #server name of gmail,port
        server.starttls() # use for security encryption
        sender_email = "amitnare4303@gmail.com" 
        sender_pass = "psgxoxgrucvnpyhe" # create password using app pass in manage gmail

        # emails = [ "1.gamil" , "2.gmail"]  use for send otp in multiple email
        receiver_email = useremail
        subject = "Your otp code "

        email_content = f"Hello user my self amit nare , use security purpose , i create otp for airline reservation project , your OTP is {otp}" 
        # f use for merge sting and interger in one message

        msg = MIMEText(email_content)
        msg ["subject"] = subject
        msg ["from"] = sender_email
        msg ["to"] = receiver_email

        server.login(sender_email,sender_pass) # use for sender login 
        server.sendmail(sender_email, receiver_email, msg.as_string()) # use for sent mail
        server.quit() # sever exit

        print("otp sent done!") # confirmation message show you on terminal 

slope().run()


