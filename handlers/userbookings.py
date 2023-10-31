import sqlite3, json, re, datetime

class UserBookings():
    def update_flight_seats(self, id):
        conn = sqlite3.connect('./data/database.db')
        c = conn.cursor()
        c.execute('SELECT available_seats FROM flights WHERE flight_id = (:id)', {
            'id':id
        })
        seat = c.fetchone()[0]
        c.execute('UPDATE flights SET available_seats = (:seats) WHERE flight_id = (:id)', {
            'id':id, 'seats': seat + 1
        })
        conn.commit()
        conn.close()
    
    def update_bookings(self, bookings, username):
        conn = sqlite3.connect('./data/database.db')
        c = conn.cursor()
        c.execute('UPDATE users SET bookings = (:bookings) WHERE username = (:username)', {
            'bookings': json.dumps(bookings), 'username': username.strip()[0].upper() + username.strip()[1:].lower()
        })
        conn.commit()
        conn.close()

    def check_bookings(self, username):
        conn = sqlite3.connect('./data/database.db')
        c = conn.cursor()
        c.execute('SELECT bookings FROM users WHERE username = (:username)', {
            'username': username.strip()[0].upper() + username.strip()[1:].lower()
        })
        record = c.fetchone()
        print(record[0])
        # for booking in json.loads(record[0]):
        #     print(booking)
        if record[0] != None:
            return json.loads(record[0])
        else: 
            return None

    def check_passengers(self, passengers):
        passengers_details = []
        conn = sqlite3.connect('./data/database.db')
        c = conn.cursor()
        for x in passengers:
            c.execute('SELECT * FROM tickets WHERE ticket_id = (:id)', {
                'id': x
            })
            record = c.fetchone()
            # print('passenger:',record)
            passengers_details.append(record)
        if passengers_details != []:
            print(passengers_details)
            return passengers_details
        else: 
            return None

    def get_full_details(self, booking):
        print('Get full details')
        print(booking)
        details = []
        i = 1
        total = 0
        passengers_details = self.check_passengers(booking['passengers'])
        # major details
        details.append(f'''Box3d:
    padding : 5, 20
    size_hint_y : None
    height : 350
    orientation : 'vertical'
    spacing : 10
    MDLabel:
        text : 'PNR : {booking['pnr']}'
        font_size: 35
        halign : "center"
        valign : "middle"
        height : 40
        size_hint_y : None
    MDLabel:
        text : 'FROM : {booking['source']}'
        font_size: 35
        halign : "center"
        valign : "middle"
        height : 40
        size_hint_y : None
    MDLabel:
        text : 'DEPARTURE ON : {booking['departure'].split(' ')[0]} AT {booking['departure'].split(' ')[1]}'
        font_size: 35
        halign : "center"
        valign : "middle"
        height : 40
        size_hint_y : None
    MDLabel:
        text : 'TO : {booking['destination']}'
        font_size: 35
        halign : "center"
        valign : "middle"
        height : 40
        size_hint_y : None
    MDLabel:
        text : 'ARRIVAL ON : {booking['arrival'].split(' ')[0]} AT {booking['arrival'].split(' ')[1]}'
        font_size: 35
        halign : "center"
        valign : "middle"
        height : 40
        size_hint_y : None
    MDLabel:
        text : 'DURATION : {int(booking['duration']) if booking['duration']*10 == int(booking['duration'])*10 else booking['duration']}HRS'
        font_size: 35
        halign : "center"
        valign : "middle"
        height : 40
        size_hint_y : None
            ''')

        # each passenger details
        for x in passengers_details:
            total += x[5]
            details.append(f'''Box3d:
    padding : 5, 20
    size_hint_y : None
    height : 240
    orientation : 'vertical'
    spacing : 10
    MDLabel:
        text : 'PASSENGER {i}'
        font_size: 28
        halign : "center"
        valign : "middle"
        height : 30
        size_hint_y : None
    MDLabel:
        text : 'Ticket ID : {x[0]}'
        font_size: 28
        halign : "center"
        valign : "middle"
        height : 30
        size_hint_y : None
    MDLabel:
        text : 'Name : {x[3]}'
        font_size: 28
        halign : "center"
        valign : "middle"
        height : 30
        size_hint_y : None
    MDLabel:
        text : 'Seat No : {x[4]}'
        font_size: 28
        halign : "center"
        valign : "middle"
        height : 30
        size_hint_y : None
    MDLabel:
        text : 'Ticket Price : Rs. {x[5]}'
        font_size: 28
        halign : "center"
        valign : "middle"
        height : 30
        size_hint_y : None
''') 
            i+=1
        # End box
        if booking['cancelled'] == False:
            details.append(f'''Box3d:
    padding : 5, 20
    size_hint_y : None
    height : 220
    orientation : 'vertical'
    spacing : 10
    MDLabel:
        text : 'TOTAL PRICE : RS. {total}'
        font_size: 35
        halign : "center"
        valign : "middle"
        height : 40
        size_hint_y : None
    MDFlatButton:
        text : 'Download Ticket'
        font_size : 35
        height : 40
        md_bg_color : 'blue'
        theme_text_color : 'Custom'
        text_color : 'white'
        pos_hint : {{'center_x':.5}}
        on_release: app.button_handler('generate-pdf',{booking})
    MDFlatButton:
        text : 'Cancel Booking'
        font_size : 35
        height : 40
        md_bg_color : 'blue'
        theme_text_color : 'Custom'
        text_color : 'white'
        pos_hint : {{'center_x':.5}}
        on_release: app.button_handler('cancel-booking',{booking})
    ''')
        else:
            details.append(f'''Box3d:
    padding : 5, 20
    size_hint_y : None
    height : 150
    orientation : 'vertical'
    spacing : 10
    MDLabel:
        text : 'TOTAL PRICE : RS. {total}'
        font_size: 35
        halign : "center"
        valign : "middle"
        height : 40
        size_hint_y : None
    MDFlatButton:
        text : 'Cancelled Booking'
        disabled : True
        font_size : 35
        height : 40
        md_bg_color : 'blue'
        theme_text_color : 'Custom'
        text_color : 'white'
        pos_hint : {{'center_x':.5}}
        on_release: app.button_handler('cancel-booking',{booking})
    ''')
        return details


    # GET EVERY BOOKING MADE BY THE USER
    def get_bookings(self, username):
        bookings = self.check_bookings(username)
        tickets = []
        if bookings != None:
            for booking in bookings:
                if booking['cancelled'] == False:
                    tickets.append(f'''Box3d:
    padding : 5, 20
    size_hint_y : None
    height : 400
    orientation : 'vertical'
    spacing : 10
    MDLabel:
        text : 'STATUS : BOOKED'
        font_size: 35
        halign : "center"
        valign : "middle"
        height : 40
        size_hint_y : None
    MDLabel:
        text : 'Booking ID : {booking['id']}'
        font_size: 28
        halign : "center"
        valign : "middle"
        height : 30
        size_hint_y : None
    MDLabel:
        text : 'PNR : {booking['pnr'].upper()}'
        font_size: 28
        halign : "center"
        valign : "middle"
        height : 30
        size_hint_y : None
    MDLabel:
        text : 'FROM : {booking['source'].upper()}'
        font_size: 18
        halign : "center"
        valign : "middle"
        height : 20
        size_hint_y : None
    MDLabel:
        text : 'TO : {booking['destination'].upper()}'
        font_size: 18
        halign : "center"
        valign : "middle"
        height : 20
        size_hint_y : None
    MDLabel:
        text : 'BOARDING DATE : {booking['departure'].split(' ')[0]}'
        font_size: 18
        halign : "center"
        valign : "middle"
        height : 20
        size_hint_y : None
    MDLabel:
        text : 'BOARDING TIME : {booking['departure'].split(' ')[1]}'
        font_size: 18
        halign : "center"
        valign : "middle"
        height : 20
        size_hint_y : None
    MDLabel:
        text : 'DURATION : {int(booking['duration']) if booking['duration']*10 == int(booking['duration'])*10 else booking['duration']} hrs'
        font_size: 18
        halign : "center"
        valign : "middle"
        height : 20
        size_hint_y : None
    MDLabel:
        text : 'NO OF PASSENGERS : {len(booking['passengers'])}'
        font_size: 18
        halign : "center"
        valign : "middle"
        height : 20
        size_hint_y : None
    MDFlatButton:
        text : 'Check Details'
        font_size : 28
        md_bg_color : 'blue'
        theme_text_color : 'Custom'
        text_color : 'white'
        pos_hint : {{'center_x':.5}}
        on_release: app.button_handler('get-booking-details',{booking})
''')
                else:
                   tickets.append(f'''Box3d:
    padding : 5, 20
    size_hint_y : None
    height : 400
    orientation : 'vertical'
    spacing : 10
    MDLabel:
        text : 'STATUS : CANCELLED'
        font_size: 35
        halign : "center"
        valign : "middle"
        height : 40
        size_hint_y : None
    MDLabel:
        text : 'Booking ID : {booking['id']}'
        font_size: 28
        halign : "center"
        valign : "middle"
        height : 30
        size_hint_y : None
    MDLabel:
        text : 'PNR : {booking['pnr'].upper()}'
        font_size: 28
        halign : "center"
        valign : "middle"
        height : 30
        size_hint_y : None
    MDLabel:
        text : 'FROM : {booking['source'].upper()}'
        font_size: 18
        halign : "center"
        valign : "middle"
        height : 20
        size_hint_y : None
    MDLabel:
        text : 'TO : {booking['destination'].upper()}'
        font_size: 18
        halign : "center"
        valign : "middle"
        height : 20
        size_hint_y : None
    MDLabel:
        text : 'BOARDING DATE : {booking['departure'].split(' ')[0]}'
        font_size: 18
        halign : "center"
        valign : "middle"
        height : 20
        size_hint_y : None
    MDLabel:
        text : 'BOARDING TIME : {booking['departure'].split(' ')[1]}'
        font_size: 18
        halign : "center"
        valign : "middle"
        height : 20
        size_hint_y : None
    MDLabel:
        text : 'DURATION : {int(booking['duration']) if booking['duration']*10 == int(booking['duration'])*10 else booking['duration']} hrs'
        font_size: 18
        halign : "center"
        valign : "middle"
        height : 20
        size_hint_y : None
    MDLabel:
        text : 'NO OF PASSENGERS : {len(booking['passengers'])}'
        font_size: 18
        halign : "center"
        valign : "middle"
        height : 20
        size_hint_y : None
    MDFlatButton:
        text : 'Check Details'
        font_size : 28
        md_bg_color : 'blue'
        theme_text_color : 'Custom'
        text_color : 'white'
        pos_hint : {{'center_x':.5}}
        on_release: app.button_handler('get-booking-details',{booking})
''')
        else:
            tickets.append(f'''Box3d:
    height : 50
    padding : 5, 10
    orientation: 'vertical'
    MDLabel:
        text: 'No Bookings Done'
        halign : 'center'
        font_size : 30
''')
        return tickets

    def textvalidator(self, type, objs):
        numreg = '[^0-9]'
        match type:     
            case 'pin':
                objs[0].text = re.sub(numreg, '', objs[0].text)
                if objs[0].text.strip() == '':
                    objs[1].disabled = True
                elif len(objs[0].text.strip()) < 6 :
                    objs[1].disabled = True
                elif len(objs[0].text.strip()) == 6 :
                    objs[1].disabled = False
                elif len(objs[0].text.strip()) > 6 :
                    objs[0].text = objs[0].text.strip()[0:-1]
    
    def validate(self, objs, id, username):
        if objs[1].text == '123456':
            self.cancel_booking(id, username)
            return True
        else:
            return False

    def cancel_booking(self, id, username):
        bookings = self.check_bookings(username)
        temp = []
        for booking in bookings:
            if booking['id'] == id:
                ticket_id = booking['passengers'][0]
                obj = booking
                obj['cancelled'] = True
                temp.append(obj)
            else:
                temp.append(booking)
        flight_id = self.check_passengers([ticket_id])[0][2]
        print(self.check_passengers([ticket_id])[0][2])
        self.update_flight_seats(flight_id)
        self.update_bookings(temp, username)
        

# print(UserBookings().get_bookings('admin'))
# d1 = datetime.datetime(2023, 10, 15, hour = 20, minute = 30)
# d2 = datetime.datetime(2023, 10, 15, hour = 23, minute = 0)
# d3 = datetime.datetime.strptime('23/10/2023 09:00:00', '%d/%m/%Y %H:%M:%S')
# print((d2 - d1).days, (d2-d1).seconds)
# print(d3)
# print(2.0*10 == 2*10)