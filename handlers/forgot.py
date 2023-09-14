import sqlite3, re
import json
import handlers.emailsender as Email
# import emailsender as Email

class ForgotPass():

    def check_password(self, username, password):
        conn = sqlite3.connect("./data/database.db")
        # conn = sqlite3.connect("../data/database.db")
        c = conn.cursor()
        c.execute("SELECT password FROM users where username = (:username)", {'username': username})
        record = c.fetchall()
        print (record, type(record))
        if record[0][0] == password:
            return True
        else:
            c = conn.cursor()
            c.execute("UPDATE users SET password = (:new) where username = (:username);", {'username' : username, 'new' : password})
            conn.commit()
            conn.close()
            return False

    def check_username(self, username):
        # connect with database
        conn = sqlite3.connect("./data/database.db")

        # create a cursor
        c = conn.cursor()

        # check details existence
        c.execute("SELECT * FROM users WHERE username = (:username)", {
            "username": username
        })

        # fetch records
        record = c.fetchall()

        if record:
            return True
        else:
            return False

    # Send email and receive the otp generated
    def send_email(self, objs):
        username = objs[0]
        code_field = objs[1]
        code_field.disabled = False
        code_field.focus = True
        # objs[2].disabled = False
        return Email.Sender().send_email('sanjiv.samal39@gmail.com')

    # Starting of validation for code sent
    def validateCode(self, obj, otp):
        obj[0].required = True
        strvalidator = self.validatetext('code', obj)
        if ( strvalidator == True ):
            x = False
            if otp == int(obj[0].text.strip()):
                x = True
            return x
        else:
            return None

    # String validation
    def validatetext(self, type, objs):
        obj = objs[0]
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

            # For code 
            case 'code':
                # print(objs[1].text)
                objs[2].disabled = True
                if(len(obj.text.strip())==0):
                    obj.error = True
                    obj.helper_text = 'Required'
                    x = False
                elif (obj.text.strip().isdigit()!=True):
                    obj.error = True
                    obj.helper_text = 'Only digits allowed'
                    x = False
                elif (len(obj.text.strip())!=4):
                    obj.error = True
                    obj.helper_text = 'Only 4 digits code allowed'
                    x = False
                else: 
                    obj.error = False
                    objs[2].disabled = False
                    x = True
            
            # For password
            case 'password':
                objs[2].disabled = True
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
                

        if type == 'username' :
            if x == True:
                y = self.check_username(username_text)
                # If the username exists in database, send code button is enabled
                if y == True:
                    objs[1].disabled = False
                else:
                    objs[1].disabled = True
            else:
                objs[1].disabled = True
        
        # if type == 'password':
        #     objs[1].disabled = False
        # if the new password and confirm new password matches create new password button is enabled
        if type == 'password' and x == True and objs[0].text == objs[1].text:
            objs[2].disabled = False

        return x

# if __name__ == "__main__":
#     ForgotPass().check_password('aayan123','Ayaan@123')
