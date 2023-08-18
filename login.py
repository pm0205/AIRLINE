from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
import sqlite3, re

Window.size = (900, 600)


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

    # Starting of validation
    def validateLogin(self, username, password):
        if (self.validatetext(username, password)==True):
            return self.checkCredentials(username.text.strip(), password.text)
        else:
            return None

    # String validation
    def validatetext(self, username, password):
        special_char = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
        username_text = username.text.strip()
        flag = True
        if(len(username_text)==0):
            username.error = True
            username.helper_text = 'Required'
            x = False
        elif(username_text[0].isdigit()==True):
            username.error = True
            username.helper_text = 'Username cannot start with a digit'
            x = False
        elif (special_char.search(username_text)!=None):
            username.error = True
            username.helper_text = 'Username can only contain alphanumeric characters'
            x = False
        elif(len(username_text) < 4):
            username.error = True
            username.helper_text = 'Atleast 4 characters required'
            x = False
        else:
            username.error = False
            x = True
        if(len(password.text)==0):
            password.error = True
            password.helper_text = 'Required'
            x = False
        return x

if __name__ == "__main__":
    LoginApp().run()
