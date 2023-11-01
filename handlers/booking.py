import datetime, re, json, sqlite3

class Booking():
    def store_booking(self, form, flight_id, username):
        conn = sqlite3.connect('./data/database.db')
        c = conn.cursor()
        # get no of tickets
        c.execute('SELECT * FROM tickets',{
        })
        record = c.fetchall()
        # ticket_id = 

    def get_total_seats(self, flight_id):
        conn = sqlite3.connect('./data/database.db')
        c = conn.cursor()
        c.execute('SELECT booked_seats, available_seats FROM flights where flight_id = (:id)', {
            'id' : flight_id
        })
        record = c.fetchone()
        print(record)
        return int(int(record[0]) + record[1])
    
    def get_booked_seats(self, flight_id):
        conn = sqlite3.connect('./data/database.db')
        c = conn.cursor()
        c.execute('SELECT seat_number FROM tickets where flight_id = (:id)', {
            'id' : flight_id
        })
        record = c.fetchall()
        data = [x[0] for x in record]
        print('Booked seats',data)
        return data

    def create_seats(self, id):
        alphabets =["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
        count = 0
        seats = []
        total_seats = self.get_total_seats(id)
        booked_seats = self.get_booked_seats(id)
        for x in alphabets:
            if count<total_seats:
                for i in range(10):
                    if f'{x}{i+1}' in booked_seats:
                        pass
                    else:
                        string = f'{x}{i+1}'
                        seats.append(string)
                    count+=1
            else:
                break
        return seats

    def create_inputs(self, passengers, id):
        details = []
        seats = self.create_seats(id)
        for i in range(passengers):
            details.append(f'''Box3d:
    padding : 5, 10
    size_hint_y : None
    height : 300
    orientation : 'vertical'
    spacing : 10
    MDLabel:
        text : 'Passenger : {i+1}'
        font_size : 28
        halign : "center"
        valign : "middle"
        height : 30
        size_hint_y : None
        # line_color: "black"
        # line_width : 1
    MDBoxLayout:
        height : 230
        spacing: 10
        padding: 0, 10
        orientation: 'vertical'
        size_hint : 1, None
        line_color : 'black'
        line_width : 1
        MDTextField:
            width: 250
            height: 30
            size_hint : None, None
            pos_hint : {{'center_x': .5}}
            icon_left: 'alphabetical-variant'
            hint_text: 'Enter your first name'
            helper_text_mode: 'on_error'
            mode: 'rectangle'
            line_color_normal: 'lightblue'
            line_color_focus: 'blue'
            padding: 10, 0
            text_color_focus: 'black'
            on_text: 
                app.strvalidator('booking', 'fname', self)
                app.update_formdetails('fname', {i}, self)
        MDTextField:
            width: 250
            height: 30
            size_hint : None, None
            pos_hint : {{'center_x': .5}}
            icon_left: 'alphabetical-variant'
            hint_text: 'Enter your last name'
            helper_text_mode: 'on_error'
            mode: 'rectangle'
            line_color_normal: 'lightblue'
            line_color_focus: 'blue'
            padding: 10, 0
            text_color_focus: 'black'
            on_text: 
                app.strvalidator('booking', 'lname', self)
                app.update_formdetails('lname', {i}, self)
        MDTextField:
            width: 250
            height: 30
            size_hint : None, None
            pos_hint : {{'center_x': .5}}
            icon_left: 'calendar-account'
            hint_text: 'Enter your age'
            helper_text_mode: 'on_error'
            mode: 'rectangle'
            line_color_normal: 'lightblue'
            line_color_focus: 'blue'
            padding: 10, 0
            text_color_focus: 'black'
            on_text: 
                app.strvalidator('booking', 'age', self)
                app.update_formdetails('age', {i}, self)
''')
        for x in seats:
            details.append(f'''Box3d:
    height : 50
    size_hint_y : None
    size_hint_x : .4
    pos_hint: {{'center_x':.5}}
    MDLabel: 
        text: '{x}'
        halign : 'center'
        size_hint_x : .6
    MDCheckbox:
        on_active: 
            app.checkbox_handler(*args, '{x}', self)
            # app.update_formdetails('checkbox', {-1}, [self, '{x}'])

''')
        return details

    # Validations
    def validate(self, obj, passengers):
        checker = True
        for i in range(len(obj.keys())-1):
            checker = checker and self.validateform('fname', obj[f'{i}']['fname'])
            checker = checker and self.validateform('lname', obj[f'{i}']['lname'])
            checker = checker and self.validateform('age', str(obj[f'{i}']['age']))
        print(checker) 
        if checker == True and len(obj['seats']) == passengers:
            return True
        else:
            return False  

    def validatePin(self, objs):
        if objs[1].text.strip()=='123456':
            return True
        else:
            return False

    def validateform(self, type, text):
        special_char = re.compile('[^a-zA-Z\d\s:]')
        num_special = re.compile('[^a-zA-Z]')
        numreg = '[^0-9]'
        x = True
        match type:
            # First name
            case 'fname':
                text = re.sub(num_special, '', text)
                if(len(text.strip())==0):
                    x = False
                elif(num_special.search(text.strip())!=None):
                    x = False
                elif(len(text.strip()) < 4 and len(text.strip())>0):
                    x = False
                else:
                    x = True

            # Last name
            case 'lname':
                text = re.sub(num_special, '', text)
                if(len(text.strip())==0):
                    x = False
                elif(num_special.search(text.strip())!=None):
                    x = False
                elif(len(text.strip()) < 4 and len(text.strip())>0):
                    x = False
                else:
                    x = True

            # Age 
            case 'age':
                text = re.sub(numreg, '', text)
                if text.strip() == '':
                    x = False
                elif re.sub('\D', '', text.strip()) == '0':
                    text = ''
                    x = False
                elif int(text.strip()) > 100 :
                    text = text.strip()[0:-1]
                    x = False
                else:
                   x = True
        return x

    def validatetext(self, type, obj):
        special_char = re.compile('[^a-zA-Z\d\s:]')
        num_special = re.compile('[^a-zA-Z]')
        numreg = '[^0-9]'
        x = True
        match type:
            # First name
            case 'fname':
                obj.text = re.sub(num_special, '', obj.text)
                if(len(obj.text.strip())==0):
                    obj.helper_text = 'Required'
                    obj.error = True
                    x = False
                elif(num_special.search(obj.text.strip())!=None):
                    obj.helper_text = 'First Name should only contain alphabets'
                    obj.error = True
                    x = False
                elif(len(obj.text.strip()) < 4 and len(obj.text.strip())>0):
                    obj.helper_text = 'Atleast 4 characters required'
                    obj.error = True
                    x = False
                else:
                    obj.error = False
                    x = True

            # Last name
            case 'lname':
                obj.text = re.sub(num_special, '', obj.text)
                if(len(obj.text.strip())==0):
                    obj.helper_text = 'Required'
                    obj.error = True
                    x = False
                elif(num_special.search(obj.text.strip())!=None):
                    obj.helper_text = 'Last Name should only contain alphabets'
                    obj.error = True
                    x = False
                elif(len(obj.text.strip()) < 4 and len(obj.text.strip())>0):
                    obj.helper_text = 'Atleast 4 characters required'
                    obj.error = True
                    x = False
                else:
                    obj.error = False
                    x = True

            # Age 
            case 'age':
                obj.text = re.sub(numreg, '', obj.text)
                if obj.text.strip() == '':
                    x = False
                elif re.sub('\D', '', obj.text.strip()) == '0':
                    obj.text = ''
                    x = False
                elif int(obj.text.strip()) > 100 :
                    obj.text = obj.text.strip()[0:-1]
                    x = False
                else:
                   x = True
            
            # Pin
            case 'pin':
                obj[0].text = re.sub(numreg, '', obj[0].text)
                if obj[0].text.strip() == '':
                    obj[1].disabled = True
                elif len(obj[0].text.strip()) < 6 :
                    obj[1].disabled = True
                elif len(obj[0].text.strip()) == 6 :
                    obj[1].disabled = False
                elif len(obj[0].text.strip()) > 6 :
                    obj[0].text = obj[0].text.strip()[0:-1]
        return x