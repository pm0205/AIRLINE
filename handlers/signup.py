import sqlite3, re

class Signup():

    def checkCredentials(self, username, email):
        # connect with database
        conn = sqlite3.connect("./data/database.db")
        # create a cursor
        a = conn.cursor()
        b = conn.cursor()
        # check details existence
        a.execute("SELECT * FROM users WHERE username = (:username)", {
            "username": username
        })
        b.execute("SELECT * FROM users WHERE mail = (:email)", {
            "email": email
        })
        # fetch records
        record1 = a.fetchall()
        record2 = b.fetchall()
        if record1 or record2:
            return True
        else:
            return False

    # Insert new record
    def new_record(self, objs):
        conn = sqlite3.connect("./data/database.db")
        c = conn.cursor()
        s = conn.cursor()
        s.execute("SELECT * FROM users")
        record = s.fetchall()
        new_id = len(record) + 1
        c.execute("INSERT INTO users (user_id, name, username, password, mail, phone, wallet) VALUES ((:id), (:name), (:username), (:password), (:email), (:phone), 0)", {'name': f'{objs[6].text.strip()} {objs[7].text.strip()}', 'username' : objs[1].text.strip(), 'password' : objs[2].text, 'email': objs[4].text.strip(), 'phone': objs[5].text.strip(), 'id': int(new_id)})
        conn.commit()
        conn.close()

    # Starting of validation for login
    def validateSignup(self, objs):
        checker = self.checkCredentials(objs[1].text.strip(), objs[4].text.strip())
        if checker == False:
            self.new_record(objs)
            return True
        else:
            return False
        
    # all fields checker
    def fields_checker(self, objs):
        checker = self.validatetext('username', objs[1]) and self.validatetext('password', objs[2]) and self.validatetext('password', objs[3]) and self.validatetext('email', objs[4]) and self.validatetext('phone', objs[5]) and self.validatetext('fname', objs[6]) and self.validatetext('lname', objs[7])

        passwords_checker = True if objs[2].text == objs[3].text else False

        if checker == True and passwords_checker == True and objs[4].error == False:
            objs[0].disabled = False
        else :
            objs[0].disabled = True

    # String validation
    def validatetext(self, type, obj):
        special_char = re.compile('[^a-zA-Z\d\s:]')
        num_special = re.compile('[^a-zA-Z]')
        email_ex = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b')
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

            # For phone number
            case 'phone':
                if(len(obj.text.strip())==0):
                    obj.error = True
                    obj.helper_text = 'Required'
                    x = False
                elif(obj.text.strip().isdigit()!=True):
                    obj.error = True
                    obj.helper_text = 'Only digits are allowed'
                    x = False
                elif(len(obj.text.strip())!=10):
                    obj.error = True
                    obj.helper_text = 'Phone number should be of only 10 digits'
                    x = False
                else: 
                    obj.error = False
                    x = True

            # For email
            case 'email':
                if(len(obj.text.strip())==0):
                    obj.error = True
                    obj.helper_text = 'Required'
                    x = False
                elif(email_ex.search(obj.text.strip())==None):
                    obj.error = True
                    obj.helper_text = 'Example: yourname@gmail.com'
                    x = False
                else:
                    obj.error = False
                    x = True
            
            # First name
            case 'fname':
                if(len(obj.text.strip())==0):
                    obj.error = True
                    obj.helper_text = 'Required'
                    x = False
                elif(num_special.search(obj.text.strip())!=None):
                    obj.error = True
                    obj.helper_text = 'First Name should only contain alphabets'
                    x = False
                elif(len(obj.text.strip()) < 4 and len(obj.text.strip())>0):
                    obj.error = True
                    obj.helper_text = 'Atleast 4 characters required'
                    x = False
                else:
                    obj.error = False
                    x = True

            # Last name
            case 'lname':
                if(len(obj.text.strip())==0):
                    obj.error = True
                    obj.helper_text = 'Required'
                    x = False
                elif(num_special.search(obj.text.strip())!=None):
                    obj.error = True
                    obj.helper_text = 'Last Name should only contain alphabets'
                    x = False
                elif(len(obj.text.strip()) < 4 and len(obj.text.strip())>0):
                    obj.error = True
                    obj.helper_text = 'Atleast 4 characters required'
                    x = False
                else:
                    obj.error = False
                    x = True
        return x

if __name__ == "__main__":
    Signup().validateSignup(['', 'Admin', 'Admin@123', 'Admin@123', 'admin@gmail.com', '1234567890', 'Admin', 'Admin'])
