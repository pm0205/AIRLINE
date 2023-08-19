from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
import sqlite3, re
import json

Window.size = (900, 600)

def update_userdata(username):
    x = {
        "username": username,
        "saved": True
        }
    f = open('./userdata.json', 'w')
    data = json.dumps(x)
    f.write(data)
    f.close()

class LoginApp():

    # on App start create/check for database file
    def connectdb(self):
        # create connection
        conn = sqlite3.connect("credential.db")

        # create cursor for cmds
        c = conn.cursor()

        # execute cmd for credentials table
        c.execute("""
                        CREATE TABLE IF NOT EXISTS credentials(
                            UID NUMBER,
                            USERNAME VARCHAR2,
                            PASSWORD VARCHAR2
                        )
                  """)

        # commit and close
        conn.commit()
        conn.close()

    def checkCredentials(self, username, password):
        # connect with database
        conn = sqlite3.connect("credential.db")

        # create a cursor
        c = conn.cursor()

        # check details existence
        c.execute("SELECT UID FROM credentials WHERE USERNAME = (:admin_user) AND PASSWORD = (:admin_pass)", {
            "admin_user": username,
            "admin_pass": password
        })

        # fetch records
        record = c.fetchall()

        if record:
            return True
        else:
            return False

    # Starting of validation for login
    def validateLogin(self, username, password, checkbox):
        username.required = True
        password.required = True
        strvalidator = self.validatetext('username', username) and self.validatetext('password', password)
        if ( strvalidator == True ):
            x = self.checkCredentials(username.text.strip(), password.text)
            if x==True and checkbox.active == True:
                update_userdata(username.text.strip())
            return x
        else:
            return None

    # String validation
    def validatetext(self, type, obj):
        special_char = re.compile('[^a-zA-Z\d\s:]')
        x = True
        match type:
            # For username
            case 'username':
                username_text = obj.text.strip()
                if(len(username_text)==0):
                    obj.error = True
                    obj.helper_text = 'Required'
                    x = False
                elif(username_text[0].isdigit()==True):
                    obj.error = True
                    obj.helper_text = 'Username cannot start with a digit'
                    x = False
                elif (special_char.search(username_text)!=None):
                    obj.error = True
                    obj.helper_text = 'Username can only contain alphanumeric characters'
                    x = False
                elif(len(username_text) < 4 and len(username_text)>0):
                    obj.error = True
                    obj.helper_text = 'Atleast 4 characters required'
                    x = False
                else:
                    obj.error = False
                    x = True
            # For password 
            case 'password':
                if(len(obj.text)==0):
                    obj.error = True
                    obj.helper_text = 'Required'
                    x = False
                elif (len(obj.text)<8 and len(obj.text)>0):
                    obj.error = True
                    obj.helper_text = 'Minimum 8 characters length'
                    x = False
                else: 
                    obj.error = False
                    x = True
        return x

if __name__ == "__main__":
    LoginApp().run()
