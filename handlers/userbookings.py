import sqlite3, json, re, datetime

class UserBookings():
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
        # on_release: app.button_handler('book-flights', None)
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
        # on_release: app.button_handler('book-flights', None)
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

# print(UserBookings().get_bookings('admin'))
# d1 = datetime.datetime(2023, 10, 15, hour = 20, minute = 30)
# d2 = datetime.datetime(2023, 10, 15, hour = 23, minute = 0)
# d3 = datetime.datetime.strptime('23/10/2023 09:00:00', '%d/%m/%Y %H:%M:%S')
# print((d2 - d1).days, (d2-d1).seconds)
# print(d3)
# print(2.0*10 == 2*10)