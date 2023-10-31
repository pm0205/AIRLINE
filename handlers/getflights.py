import sqlite3
import json
import re
from kivy.lang import Builder
from kivymd.uix.label import MDLabel, MDIcon
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.button import MDRectangleFlatButton, MDFlatButton, MDRaisedButton, MDTextButton, MDFillRoundFlatButton
from kivymd.uix.behaviors import (RectangularRippleBehavior,
    FakeRectangularElevationBehavior, CommonElevationBehavior,
    BackgroundColorBehavior)

# class CommonElevationBehavior():
#     def __init__(self, *args, **kwargs):
#         pass

class Box3d(CommonElevationBehavior, MDBoxLayout):
    pass

class GetFlights():
    def get_flights(self, dep, arv, date):
        conn = sqlite3.connect('./data/database.db')
        c = conn.cursor()
        c.execute('SELECT * FROM flights WHERE departure_airport = (:dep) AND arrival_airport = (:arv)', {
            'dep': dep,
            'arv': arv
        })
        records = c.fetchall()
        # print(records)
        data = []
        if records:
            for record in records:
                if date in record[5]:
                    print(type(record[5]))
                    data.append(record)
        return data
        # conn.commit()
        # conn.close()

    def get_results(self, dep, arv, date, passengers):
        dep = dep.strip().upper()
        arv = arv.strip().upper()
        date = date.split(' / ')
        # date = reversed(date)
        date = '/'.join(date)
        print(date)
        passengers = int(passengers)
        data = self.get_flights(dep, arv, date)
        flights = []
        if data != []:
            print(data)
            for x in data:
                flights.append(f'''Box3d:
    padding : 5, 10
    size_hint_y : None
    height : 250
    orientation : 'vertical'
    spacing : 10
    MDLabel:
        text : '{x[2].strip()}'
        font_size: 28
        halign : "center"
        valign : "middle"
        height : 30
        size_hint_y : None
        # line_color: "black"
        # line_width : 1
    MDFloatLayout:
        height : 30
        size_hint : 1, None
        # line_color : 'black'
        # line_width : 1
        MDLabel:
            text: '{x[3].strip()}'
            halign : 'center'
            pos_hint : {{'x': .03, 'center_y': .5}}
            adaptive_size : True
        MDLabel:
            text: '{x[4].strip()}'
            halign : 'center'
            pos_hint : {{'right': .97, 'center_y': .5}}
            adaptive_size : True
    MDFloatLayout:
        height : 30
        size_hint : 1, None
        # line_color : 'black'
        # line_width : 1
        MDLabel:
            text: '{x[5]}'
            pos_hint : {{'x': .03, 'center_y': .5}}
            adaptive_size : True
        MDLabel:
            text: '{x[6]}'
            pos_hint : {{'right': .97, 'center_y': .5}}
            adaptive_size : True
    MDLabel:
        text : 'Rs. {passengers*int(x[9])}'
        halign : 'center'
        font_size : 28
        pos_hint : {{'center_x':.5}}
        size_hint : 1, None
        height : 30
        # line_color : 'black'
        # line_width : 1
    MDFlatButton:
        text : 'Book Now'
        font_size : 28
        md_bg_color : 'blue'
        theme_text_color : 'Custom'
        text_color : 'white'
        pos_hint : {{'center_x':.5}}
        on_release: app.button_handler('book-flights', {[x, passengers]})
''')
        else:
            flights.append(f'''Box3d:
    height : 50
    padding : 5, 10
    orientation: 'vertical'
    MDLabel:
        text: 'No Flights Available'
        halign : 'center'
        font_size : 30
''')
        # print(flights)
        return flights
