import json, sqlite3, re
import handlers.emailsender as Email

def load_user_data():
    f = open('./data/userdata.json')
    data = json.load(f)
    f.close()
    return data

class UserDetails():
    def check_user_details(self, username):
        conn = sqlite3.connect("./data/database.db")
        c = conn.cursor()
        username_valid = username.strip()[0].upper() + username.strip()[1:].lower()
        c.execute("SELECT * FROM users WHERE username = (:username)", {
            "username": username_valid
        })
        # fetch records
        record = c.fetchall()
        print(record[0])
        # (6, 'Admin Admin', 'Admin', 'Admin@12345', 'admin@gmail.com', '1234567890', None, None, 100)
        return record[0]
    
    def get_user_details(self, getter, username):
        data = self.check_user_details(username)
        match getter:
            case 'email':
                return data[4].text.strip()
            case 'username':
                return data[2].text.strip()[0].upper() + data[2].text.strip()[1:].upper()

    def check_username(self, username):
        conn = sqlite3.connect("./data/database.db")
        c = conn.cursor()
        c.execute("SELECT username FROM users WHERE username = (:username)", {
            "username": f'{username.strip()[0].upper()}{username.strip()[1:].lower()}',
        })
        record = c.fetchall()
        return record
    
    def check_email(self, email):
        conn = sqlite3.connect('./data/database.db')
        c = conn.cursor()
        c.execute("SELECT mail FROM users WHERE mail = (:email)", {
            "email": f'{email.strip()}',
        })
        record = c.fetchone()
        print(record)
        if record == None:
            return False
        else:
            return True
    
    def check_password(self, username, password):
        conn = sqlite3.connect("./data/database.db")
        # conn = sqlite3.connect("../data/database.db")
        c = conn.cursor()
        c.execute("SELECT password FROM users where username = (:username)", {
            'username': username.strip()[0].upper() + username.strip()[1:].lower()
        })
        record = c.fetchall()
        print (record, type(record))
        if record[0][0] == password:
            return True
        else:
            c = conn.cursor()
            c.execute("UPDATE users SET password = (:new) where username = (:username);", {
                'username' : username.strip()[0].upper() + username.strip()[1:].lower(), 
                'new' : password
            })
            conn.commit()
            conn.close()
            return False

    def send_email(self, objs):
        objs[0].disabled = True
        objs[1].disabled = False
        objs[1].focus = True
        return Email.Sender().send_email('sanjiv.samal39@gmail.com')
    
    def update_userdetails(self, objs, username):
        conn = sqlite3.connect("./data/database.db")
        c = conn.cursor()
        c.execute("UPDATE users SET name = (:name), username = (:new_username), phone = (:phone), gender = (:gender), address = (:address) where username = (:username);", {'username' : username, 
            'name' : f'{objs[0].text.strip()[0].upper()}{objs[0].text.strip()[1:].lower()} {objs[1].text.strip()[0].upper()}{objs[1].text.strip()[1:].lower()}', 
            'new_username': f'{objs[2].text.strip()[0].upper()}{objs[2].text.strip()[1:].lower()}',
            'phone': objs[3].text.strip(),
            'gender': objs[4].text.strip().upper() if len(objs[4].text.strip())>0 else None,
            'address': objs[5].text if len(objs[5].text.strip())>0 else None
            })
        conn.commit()
        conn.close()
    
    def update_email(self, username, email):
        conn = sqlite3.connect('./data/database.db')
        c = conn.cursor()
        c.execute('UPDATE users SET mail = (:email) WHERE username = (:username);', {
            'username': f'{username.strip()[0].upper()}{username.strip()[1:].lower()}',
            'email': email.text.strip().lower(),
        })
        conn.commit()
        conn.close()

    def fill_details(self, objs, values):
        # (6, 'Admin Admin', 'Admin', 'Admin@12345', 'admin@gmail.com', '1234567890', None, None, 100)
        objs[0].text = values[1].split()[0].strip()
        objs[1].text = values[1].split()[1].strip()
        objs[2].text = values[2].strip()
        objs[3].text = values[5].strip()
        if values[6]==None:
            objs[4].text = ''
        else:
            objs[4].text = values[6].strip()
        if values[7]==None:
            objs[4].text = ''
        else:
            objs[5].text = values[7]
        objs[6].text = values[4].strip()

    def validate(self, objs, button, username):
        checker = self.validateText('fname',objs[0]) and self.validateText('lname',objs[1]) and self.validateText('username', objs[2]) and self.validateText('phone', objs[3]) and self.validateText('gender', objs[4]) and self.validateText('address', objs[5])
        if checker == True:
            if objs[2].text.strip().lower() != username.lower():
                if len(self.check_username(objs[2].text.strip())) == 0:
                    self.update_userdetails(objs, username)
                    return True
                else:
                    return 'Username already exists'
            else:
                self.update_userdetails(objs, username)
                return True
        else:
            return None

 # Starting of validation for code sent
    def validateCode(self, obj, otp):
        strvalidator = self.validateText('code', obj)
        if ( strvalidator == True ):
            x = False
            if otp == int(obj[0].text.strip()):
                x = True
            return x
        else:
            return None

    def validateText(self, type, obj):
        special_char = re.compile('[^a-zA-Z\d\s:]')
        num_special = re.compile('[^a-zA-Z]')
        email_ex = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b')
        gender_ex = re.compile('[mfoMFO]')
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
                email = obj[0]
                if(len(email.text.strip())==0):
                    email.error = True
                    email.helper_text = 'Required'
                    x = False
                    obj[1].disabled = True
                elif(email_ex.search(email.text.strip())==None):
                    email.error = True
                    email.helper_text = 'Example: yourname@gmail.com'
                    x = False
                    obj[1].disabled = True
                else:
                    email.error = False
                    x = True
                    obj[1].disabled = False
            
            # Code
            case 'code':
                code = obj[0]
                obj[1].disabled = True
                if(len(code.text.strip())==0):
                    code.error = True
                    code.helper_text = 'Required'
                    x = False
                elif (code.text.strip().isdigit()!=True):
                    code.error = True
                    code.helper_text = 'Only digits allowed'
                    x = False
                elif (len(code.text.strip())!=4):
                    code.error = True
                    code.helper_text = 'Only 4 digits code allowed'
                    x = False
                else: 
                    code.error = False
                    obj[1].disabled = False
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
            
            # Gender
            case 'gender':
                if obj.text.strip() == '':
                    obj.text = ''
                elif gender_ex.search(obj.text[len(obj.text.strip()) - 1]) != None:
                    obj.text = obj.text[len(obj.text.strip())-1].upper()
                elif len(obj.text) == 1:
                    if gender_ex.search(obj.text[len(obj.text.strip()) - 1]) != None:
                        obj.text = obj.text.upper()
                    else:
                        obj.text = ''
                else:
                    obj.text = obj.text[0]
                    
            # Address
            case 'address':
                if len(obj.text)>200:
                    obj.error = True
                    obj.helper_text = 'Max 200 characters'
                    x = False
                else:
                    obj.error = False
                    x = True

        return x
