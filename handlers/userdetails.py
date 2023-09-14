import json, sqlite3

def load_user_data():
    f = open('./data/userdata.json')
    data = json.load(f)
    f.close()
    return data

class UserDetails():
    def check_user_details(self, username):
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
        print(record[0])
        return record[0]
    
    def fill_details(self, objs, values):
        # (6, 'Admin Admin', 'Admin', 'Admin@1234', 'admin@gmail.com', '1234567890', None, None)
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

    def validateText(self, type, obj, button):
        special_char = re.compile('[^a-zA-Z\d\s:]')
        num_special = re.compile('[^a-zA-Z]')
        email_ex = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b')
        x = True
        button.disabled = True
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
                    button.disabled = False

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
                    button.disabled = False

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
                    button.disabled = False

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
                    button.disabled = False
            
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
                    button.disabled = False

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
                    button.disabled = False

        return x
