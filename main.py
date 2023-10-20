from kivymd.app import MDApp
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager
from kivymd.uix.dialog import MDDialog
from kivy.animation import Animation
from kivymd.uix.label import MDLabel, MDIcon
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.list import OneLineListItem, TwoLineListItem
from kivymd.uix.button import MDRectangleFlatButton, MDFlatButton, MDRaisedButton, MDTextButton, MDFillRoundFlatButton
from kivy.uix.button import Button
from kivymd.uix.behaviors import (RectangularRippleBehavior,
                                  FakeRectangularElevationBehavior, CommonElevationBehavior,
                                  BackgroundColorBehavior)
from kivy.uix.behaviors import ButtonBehavior

# All handler scripts
import handlers.login as Login
import handlers.pnrChecker as PnrChecker
import handlers.forgot as Forgot
import handlers.signup as Signup
import handlers.searchflight as SearchFlight
import handlers.getflights as GetFlights
import handlers.userdetails as UserDetails
import handlers.userwallet as UserWallet
import handlers.userbookings as UserBookings

# Python modules
import json
import time
import datetime
from functools import partial

#


def check_saved_data():
    f = open('./data/userdata.json')
    data = json.load(f)
    f.close()
    if len(data['username'].strip()) > 0:
        return data['saved']
    else:
        return False


def load_user_data():
    f = open('./data/userdata.json')
    data = json.load(f)
    f.close()
    if len(data['username'].strip()) > 0:
        return data
    else:
        return None


def update_user_data(username, islogin=False):
    f = open('./data/userdata.json')
    data = json.load(f)
    f.close()
    obj = {
        'username': username,
        'saved': data['saved'],
        'islogin': islogin
    }
    w = open('./data/userdata.json', 'w')
    w.write(json.dumps(obj))
    w.close()


def load_airports_data():
    f = open('./data/airports.json')
    data = json.load(f)
    data = [x for x in data if x['type'] == 'airport' and x['name'] != None]
    f.close()
    return data


def remove_children(obj):
    children = [child for child in obj.children]
    if children:
        for child in children:
            obj.remove_widget(child)


def adjust_height(obj):
    padding = obj.padding[1]
    spacing = obj.spacing
    obj.height = 2*padding
    children = [child for child in obj.children]
    if children:
        for child in children:
            obj.height += child.height
            obj.height += spacing
    obj.height = f'{obj.height}sp'


key_pressed = None
key_modifier = None

# Build components


class DialogContent(MDFloatLayout):
    pass


class NotificationBox(CommonElevationBehavior, MDBoxLayout):
    pass


class Box3d(CommonElevationBehavior, MDBoxLayout):
    pass


class ElevButton(FakeRectangularElevationBehavior, MDFillRoundFlatButton):
    pass


class MyKeyboardListener(Widget):
    def __init__(self, **kwargs):
        super(MyKeyboardListener, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(
            self._keyboard_closed, self, 'text')
        if self._keyboard.widget:
            # If it exists, this widget is a VKeyboard object which you can use
            # to change the keyboard layout.
            pass
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def _keyboard_closed(self):
        print('My keyboard have been closed!')
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        global key_pressed, key_modifier
        key_pressed = keycode[1]
        key_modifiers = modifiers
        print('The key', keycode[1], 'have been pressed')
        print(' - text is %r' % text)
        print(' - modifiers are %r' % modifiers)

        # Keycode is composed of an integer + a string
        # If we hit escape, release the keyboard
        # if keycode[1] == 'escape':
        #     keyboard.release()

        # Return True to accept the key. Otherwise, it will be used by
        # the system.
        return True

# Main APP code starts here ................................................................................


class MainApp(MDApp):
    dialog = None
    menu = None

    # pre-load all screens
    def load_all_files(self):
        # HOME TAB
        self.screen_manager.get_screen('main screen').ids.homescreen_manager.add_widget(
            Builder.load_file('./screens/homescreen.kv'))
        self.screen_manager.get_screen('main screen').ids.homescreen_manager.add_widget(
            Builder.load_file('./screens/pnrscreen.kv'))
        self.screen_manager.get_screen('main screen').ids.homescreen_manager.add_widget(
            Builder.load_file('./screens/loginscreen.kv'))
        self.screen_manager.get_screen('main screen').ids.homescreen_manager.add_widget(
            Builder.load_file('./screens/signupscreen.kv'))
        # self.screen_manager.get_screen('main screen').ids.homescreen_manager.add_widget(Builder.load_file('./screens/loadingscreen.kv'))
        self.screen_manager.get_screen('main screen').ids.homescreen_manager.add_widget(
            Builder.load_file('./screens/forgotpasswordscreen.kv'))
        self.screen_manager.get_screen('main screen').ids.homescreen_manager.add_widget(
            Builder.load_file('./screens/newpasswordscreen.kv'))
        self.screen_manager.get_screen('main screen').ids.homescreen_manager.add_widget(
            Builder.load_file('./screens/getflightsscreen.kv'))

        # USER TAB
        self.screen_manager.get_screen('main screen').ids.userscreen_manager.add_widget(
            Builder.load_file('./screens/userscreen.kv'))
        # details
        self.screen_manager.get_screen('main screen').ids.userscreen_manager.add_widget(
            Builder.load_file('./screens/userdetailsscreen.kv'))
        self.screen_manager.get_screen('main screen').ids.userscreen_manager.add_widget(
            Builder.load_file('./screens/updateemailscreen.kv'))
        self.screen_manager.get_screen('main screen').ids.userscreen_manager.add_widget(
            Builder.load_file('./screens/updatepasswordscreen.kv'))
        # wallet
        self.screen_manager.get_screen('main screen').ids.userscreen_manager.add_widget(
            Builder.load_file('./screens/userwalletscreen.kv'))
        self.screen_manager.get_screen('main screen').ids.userscreen_manager.add_widget(
            Builder.load_file('./screens/updatewalletscreen.kv'))
        self.screen_manager.get_screen('main screen').ids.userscreen_manager.add_widget(
            Builder.load_file('./screens/updatewalletupiscreen.kv'))
        # bookings
        self.screen_manager.get_screen('main screen').ids.userscreen_manager.add_widget(
            Builder.load_file('./screens/userbookingsscreen.kv'))
        self.screen_manager.get_screen('main screen').ids.userscreen_manager.add_widget(
            Builder.load_file('./screens/userbookingdetailsscreen.kv'))

        # Check if login was details were saved to auto-login
        userdata = load_user_data()
        if check_saved_data() == True:
            remove_children(self.screen_manager.get_screen(
                'main screen').ids.homescreen_manager.get_screen('home screen').ids.home_top_right_box)
            self.screen_manager.get_screen('main screen').ids.homescreen_manager.get_screen(
                'home screen').ids.home_top_right_box.add_widget(MDIcon(icon='account', size_hint_x=.1))
            self.screen_manager.get_screen('main screen').ids.homescreen_manager.get_screen(
                'home screen').ids.home_top_right_box.add_widget(MDLabel(text=userdata['username'], halign='center', adaptive_height=True))
            self.homescreenchanger('home screen')

    def build(self):
        self.theme_cls.theme_style = 'Light'  # or 'Dark'
        self.theme_cls.primary_palette = 'Blue'
        self.icon = "./assets/icon.ico"
        self.screen_manager = ScreenManager()
        self.screen_manager.add_widget(
            Builder.load_file('./screens/windowscreen.kv'))
        self.load_all_files()
        self.notification_box = self.screen_manager.get_screen(
            'main screen').ids.notification_box
        self.notification_text = self.screen_manager.get_screen(
            'main screen').ids.notification_text
        return self.screen_manager

    def on_start(self):

        self.title = "Eagle Airline | Ticket Booking System"
        self.show_alert_dialog('loading', '')
        # self.homescreenchanger('home - flights')
        # self.userscreenchanger('home - details')

        # Shortnaming screens
        # Homescreens
        self.homescreen_get_flights = self.screen_manager.get_screen(
            'main screen').ids.homescreen_manager.get_screen('get flights screen')
        
        # Userscreens
        self.userscreen_home = self.screen_manager.get_screen(
            'main screen').ids.userscreen_manager.get_screen('user home screen')
        self.userscreen_details = self.screen_manager.get_screen(
            'main screen').ids.userscreen_manager.get_screen('user details screen')
        self.userscreen_email = self.screen_manager.get_screen(
            'main screen').ids.userscreen_manager.get_screen('user email screen')
        self.userscreen_password = self.screen_manager.get_screen(
            'main screen').ids.userscreen_manager.get_screen('user password screen')
        self.userscreen_wallet = self.screen_manager.get_screen(
            'main screen').ids.userscreen_manager.get_screen('user wallet screen')
        self.userscreen_update_wallet = self.screen_manager.get_screen(
            'main screen').ids.userscreen_manager.get_screen('update wallet screen')
        self.userscreen_update_wallet_upi = self.screen_manager.get_screen(
            'main screen').ids.userscreen_manager.get_screen('update wallet upi screen')
        self.userscreen_bookings = self.screen_manager.get_screen(
            'main screen').ids.userscreen_manager.get_screen('user bookings screen')
        self.userscreen_bookings_details = self.screen_manager.get_screen(
            'main screen').ids.userscreen_manager.get_screen('user booking details screen')

        # Pre load user data if available
        self.fill_user_data()

    # Fill user details
    def fill_user_data(self, *args, **kwargs):
        user_data = load_user_data()
        if user_data:
            if user_data['saved'] == True:
                update_user_data(user_data['username'], islogin=True)
            elif user_data['saved'] == False:
                update_user_data(user_data['username'], islogin=False)

            # User details
            data = UserDetails.UserDetails().check_user_details(user_data['username'].strip()[
                0].upper() + user_data['username'].strip()[1:].lower())
            self.username = data[2].strip()[0].upper() + \
                data[2].strip()[1:].lower()
            self.email = data[4].strip().lower()
            self.wallet = str(data[8])
            print(self.wallet)
            self.userscreen_wallet.ids.user_wallet_amount.text = 'Rs ' + self.wallet
            self.userscreen_home.ids.user_homescreen_name.text = data[1].split(' ')[
                0]
            UserDetails.UserDetails().fill_details([self.userscreen_details.ids.user_details_fname, self.userscreen_details.ids.user_details_lname, self.userscreen_details.ids.user_details_username,
                                                    self.userscreen_details.ids.user_details_phone, self.userscreen_details.ids.user_details_gender, self.userscreen_details.ids.user_details_address, self.userscreen_details.ids.user_details_email], data)
            
            # User Bookings
            bookings = UserBookings.UserBookings().get_bookings(user_data['username'])
            box = self.screen_manager.get_screen('main screen').ids.userscreen_manager.get_screen(
                'user bookings screen').ids.user_bookings_main_box
            remove_children(box)
            for booking in bookings:
                box.add_widget(Builder.load_string(booking))
                adjust_height(box)
                adjust_height(self.userscreen_bookings.ids.user_bookings_outer_box)
            # self.userscreenchanger('home - bookings')

    # Reset a screen elements back to default
    def reset_screen(self, screen_name, objs=None, *args, **kwargs):
        match screen_name:
            case 'login':
                pass
            case 'signup':
                pass
            case 'forgot password':
                pass
            case 'new email':
                objs[2].text = ''
                objs[3].disabled = True
                objs[2].disabled = False
                objs[1].disabled = True
                objs[0].disabled = True
                objs[0].text = ''
            case 'update password':
                self.userscreen_password.ids.update_password_email.text = 'Click on Send Code to receive code on your email and then Verify the code Sent'
                self.userscreen_password.ids.update_password_code_field.text = ''
                self.userscreen_password.ids.update_password_code_field.disabled = True
                self.userscreen_password.ids.update_password_code_field.error = False
                self.userscreen_password.ids.update_password_confirmcode_btn.disabled = True
                self.userscreen_password.ids.update_password_btn.disabled = True
                self.userscreen_password.ids.update_password1.text = ''
                self.userscreen_password.ids.update_password1.error = False
                self.userscreen_password.ids.update_password2.text = ''
                self.userscreen_password.ids.update_password2.error = False
            case 'update wallet upi':
                self.userscreen_update_wallet_upi.ids.update_wallet_upi_pin.text = ''
                self.userscreen_update_wallet_upi.ids.update_wallet_upi_amount.text = 'Rs '
                self.userscreen_update_wallet_upi.ids.update_wallet_upi_pin.error = False
                self.userscreen_update_wallet_upi.ids.update_wallet_upi_paybtn.disabled = True

    # Change tabs

    def tab_changer(self, obj):
        user = load_user_data()
        if user:
            if user['saved'] == False:
                self.screen_manager.get_screen(
                    'main screen').ids.tab_navigator.switch_tab('home')
                self.show_notification('Please login first to access')
            elif user['saved'] == True:
                self.screen_manager.get_screen(
                    'main screen').ids.tab_navigator.switch_tab('account')
        # else:
            # self.show_notification('Please login first to access')
            # self.screen_manager.get_screen('main screen').ids.tab_navigator.switch_tab('home')

    # Screen Changers
    # USER SCREEN
    def userscreenchanger(self, screen_name, *args, **kwargs):
        match screen_name:
            case 'home - details':
                self.screen_manager.get_screen(
                    'main screen').ids.userscreen_manager.current = 'user details screen'
                self.screen_manager.get_screen(
                    'main screen').ids.userscreen_manager.transition.direction = 'left'
            case 'details - home':
                self.screen_manager.get_screen(
                    'main screen').ids.userscreen_manager.current = 'user home screen'
                self.screen_manager.get_screen(
                    'main screen').ids.userscreen_manager.transition.direction = 'right'
            case 'details - email':
                self.screen_manager.get_screen(
                    'main screen').ids.userscreen_manager.current = 'user email screen'
                self.screen_manager.get_screen(
                    'main screen').ids.userscreen_manager.transition.direction = 'up'
            case 'details - password':
                self.screen_manager.get_screen(
                    'main screen').ids.userscreen_manager.current = 'user password screen'
                self.screen_manager.get_screen(
                    'main screen').ids.userscreen_manager.transition.direction = 'up'
            case 'home - wallet':
                self.screen_manager.get_screen(
                    'main screen').ids.userscreen_manager.current = 'user wallet screen'
                self.screen_manager.get_screen(
                    'main screen').ids.userscreen_manager.transition.direction = 'left'
            case 'wallet - update wallet':
                self.screen_manager.get_screen(
                    'main screen').ids.userscreen_manager.current = 'update wallet screen'
                self.screen_manager.get_screen(
                    'main screen').ids.userscreen_manager.transition.direction = 'up'
            case 'update wallet - upi':
                self.screen_manager.get_screen(
                    'main screen').ids.userscreen_manager.current = 'update wallet upi screen'
                self.screen_manager.get_screen(
                    'main screen').ids.userscreen_manager.transition.direction = 'up'
            case 'home - bookings':
                self.screen_manager.get_screen(
                    'main screen').ids.userscreen_manager.current = 'user bookings screen'
                self.screen_manager.get_screen(
                    'main screen').ids.userscreen_manager.transition.direction = 'left'
            case 'bookings - details':
                self.screen_manager.get_screen(
                    'main screen').ids.userscreen_manager.current = 'user booking details screen'
                self.screen_manager.get_screen(
                    'main screen').ids.userscreen_manager.transition.direction = 'left'

            case 'back - home':
                self.screen_manager.get_screen(
                    'main screen').ids.userscreen_manager.current = 'user home screen'
                self.screen_manager.get_screen(
                    'main screen').ids.userscreen_manager.transition.direction = 'right'

    # HOME SCREEN
    def homescreenchanger(self, screen_name):
        match screen_name:
            case 'pnr screen':
                self.screen_manager.get_screen(
                    'main screen').ids.homescreen_manager.current = 'pnr screen'
                self.screen_manager.get_screen(
                    'main screen').ids.homescreen_manager.transition.direction = 'left'
            case 'login screen':
                self.screen_manager.get_screen(
                    'main screen').ids.homescreen_manager.current = 'login screen'
                self.screen_manager.get_screen(
                    'main screen').ids.homescreen_manager.transition.direction = 'down'
                Clock.schedule_once(partial(self.text_anim, 'login', 'L'), 0.5)
                Clock.schedule_once(partial(self.text_anim, 'login', 'LO'), 1)
                Clock.schedule_once(
                    partial(self.text_anim, 'login', 'LOG'), 1.5)
                Clock.schedule_once(
                    partial(self.text_anim, 'login', 'LOGI'), 2)
                Clock.schedule_once(
                    partial(self.text_anim, 'login', 'LOGIN'), 2.5)
            case 'signup screen':
                self.screen_manager.get_screen(
                    'main screen').ids.homescreen_manager.current = 'signup screen'
                self.screen_manager.get_screen(
                    'main screen').ids.homescreen_manager.transition.direction = 'down'
                Clock.schedule_once(
                    partial(self.text_anim, 'signup', 'S'), 0.5)
                Clock.schedule_once(partial(self.text_anim, 'signup', 'SI'), 1)
                Clock.schedule_once(
                    partial(self.text_anim, 'signup', 'SIG'), 1.5)
                Clock.schedule_once(
                    partial(self.text_anim, 'signup', 'SIGN'), 2)
                Clock.schedule_once(
                    partial(self.text_anim, 'signup', 'SIGN '), 2.5)
                Clock.schedule_once(
                    partial(self.text_anim, 'signup', 'SIGN U'), 3)
                Clock.schedule_once(
                    partial(self.text_anim, 'signup', 'SIGN UP'), 3.5)
            case 'login-signup':
                self.screen_manager.get_screen(
                    'main screen').ids.homescreen_manager.current = 'signup screen'
                self.screen_manager.get_screen(
                    'main screen').ids.homescreen_manager.transition.direction = 'left'
            case 'home screen':
                self.screen_manager.get_screen(
                    'main screen').ids.homescreen_manager.current = 'home screen'
                self.screen_manager.get_screen(
                    'main screen').ids.homescreen_manager.transition.direction = 'right'
            case 'forgot screen':
                # reseting all elements
                self.screen_manager.get_screen('main screen').ids.homescreen_manager.get_screen(
                    'forgotpassword screen').ids.forgotusername.disabled = False
                self.screen_manager.get_screen('main screen').ids.homescreen_manager.get_screen(
                    'forgotpassword screen').ids.forgotusername.text = ''
                self.screen_manager.get_screen('main screen').ids.homescreen_manager.get_screen(
                    'forgotpassword screen').ids.code_field.disabled = True
                self.screen_manager.get_screen('main screen').ids.homescreen_manager.get_screen(
                    'forgotpassword screen').ids.code_field.text = ''
                self.screen_manager.get_screen('main screen').ids.homescreen_manager.get_screen(
                    'forgotpassword screen').ids.sendcode_button.disabled = True
                self.screen_manager.get_screen('main screen').ids.homescreen_manager.get_screen(
                    'forgotpassword screen').ids.confirmcode_btn.disabled = True
                # transition of screen
                self.screen_manager.get_screen(
                    'main screen').ids.homescreen_manager.current = 'forgotpassword screen'
                self.screen_manager.get_screen(
                    'main screen').ids.homescreen_manager.transition.direction = 'up'
            case 'new password screen':
                # reset widgets
                self.screen_manager.get_screen('main screen').ids.homescreen_manager.get_screen(
                    'new password screen').ids.new_password1.text = ''
                self.screen_manager.get_screen('main screen').ids.homescreen_manager.get_screen(
                    'new password screen').ids.new_password2.text = ''
                self.screen_manager.get_screen('main screen').ids.homescreen_manager.get_screen(
                    'new password screen').ids.confirmpassword_btn.disabled = True
                # screen transition
                self.screen_manager.get_screen(
                    'main screen').ids.homescreen_manager.current = 'new password screen'
                self.screen_manager.get_screen(
                    'main screen').ids.homescreen_manager.transition.direction = 'left'
            case 'new password - home':
                # reset widgets
                self.screen_manager.get_screen('main screen').ids.homescreen_manager.get_screen(
                    'new password screen').ids.new_password1.text = ''
                self.screen_manager.get_screen('main screen').ids.homescreen_manager.get_screen(
                    'new password screen').ids.new_password2.text = ''
                self.screen_manager.get_screen('main screen').ids.homescreen_manager.get_screen(
                    'new password screen').ids.confirmpassword_btn.disabled = True
                # screen transition
                self.screen_manager.get_screen(
                    'main screen').ids.homescreen_manager.current = 'home screen'
                self.screen_manager.get_screen(
                    'main screen').ids.homescreen_manager.transition.direction = 'up'
            case 'home - flights':
                self.screen_manager.get_screen(
                    'main screen').ids.homescreen_manager.current = 'get flights screen'
                self.screen_manager.get_screen(
                    'main screen').ids.homescreen_manager.transition.direction = 'left'

    # Button handler
    def button_handler(self, work, objs):
        match work:
            case 'book-flights':
                print("Book flight")
                if load_user_data()['islogin'] == True:
                    pass
                else:
                    Clock.schedule_once(partial(self.show_notification, 'Login first to book a flight', notifier=[self.homescreen_get_flights.ids.get_flights_notification_box, self.homescreen_get_flights.ids.get_flights_notification_text]), .2)
                    # self.show_alert_dialog()
            
            # User Screen
            case 'edit-details':
                for x in objs[1:]:
                    x.disabled = False
                objs[1].focus = True
            case 'newemail-send-code':
                x = UserDetails.UserDetails().check_email(objs[1].text.strip())
                # if email already exists
                if x == True:
                    self.show_notification(text='Email already exists', notifier=[self.userscreen_email.ids.new_email_notification_box, self.userscreen_email.ids.new_email_notification_text])
                else:
                    objs[1].disabled = True
                    # stores username in the class so as to use it to push the new password created to the particular record
                    self.username = objs[1].text.strip()[0].upper(
                    ) + objs[1].text.strip()[1:].lower()
                    self.otp = UserDetails.UserDetails().send_email(objs[1:])
                    revrange = list(range(0, 11))
                    revrange.reverse()
                    # print(revrange)
                    for i in revrange:
                        Clock.schedule_once(
                            partial(self.codebutton_timer, objs[0], i), float(10 - i + .5))
            case 'update-password-send-code':
                email = self.email
                self.otp = UserDetails.UserDetails().send_email(objs)
                revrange = list(range(0, 11))
                revrange.reverse()
                # print(revrange)
                Clock.schedule_once(
                    partial(self.text_anim, 'update password email'), 4)
                for i in revrange:
                    Clock.schedule_once(
                        partial(self.codebutton_timer, objs[0], i), float(10 - i + .5))

            case 'get-booking-details':
                details = UserBookings.UserBookings().get_full_details(objs)
                remove_children(self.userscreen_bookings_details.ids.user_booking_details_main_box)
                self.userscreen_bookings_details.ids.user_booking_details_heading.text = 'BOOKING DETAILS FOR : ' + objs['pnr']
                box = self.userscreen_bookings_details.ids.user_booking_details_main_box
                for detail in details:
                    box.add_widget(Builder.load_string(detail))
                    adjust_height(box)
                    adjust_height(self.userscreen_bookings_details.ids.user_booking_details_outer_box)
                self.userscreenchanger('bookings - details')

    # Input validation when button is clicked
    def validate(self, type, obj):
        match type:
            # Home screen
            case 'login':
                x = Login.LoginApp().validateLogin(obj[0], obj[1], obj[2])
                if (x == True) or (x == False):
                    self.show_alert_dialog('login', x)
                else:
                    pass
            case 'signup':
                x = Signup.Signup().validateSignup(obj)
                self.show_alert_dialog('signup', x)
            case 'pnr':
                x = PnrChecker.PnrChecker().validatePnr(obj)
                if x != False:
                    # self.show_alert_dialog('loading', '')
                    self.show_alert_dialog('pnr', x)
            case 'forgot password':
                x = Forgot.ForgotPass().validateCode(obj, self.otp)
                if (x == True) or (x == False):
                    self.show_alert_dialog('forgot password', x)
                else:
                    pass
            case 'confirm password':
                x = Forgot.ForgotPass().check_password(
                    self.username, obj[1].text)
                self.show_alert_dialog('new password', x)
            case 'search flights':
                x = SearchFlight.Search().validate(obj)
                box = self.screen_manager.get_screen('main screen').ids.homescreen_manager.get_screen(
                    'get flights screen').ids.get_flights_main_box
                remove_children(box)
                if x == True:
                    datas = GetFlights.GetFlights().get_results(
                        obj[1].text, obj[2].text, obj[3].text, obj[4].text)
                    self.text_anim(
                        type='flights', string=f'{obj[1].text} >> {obj[2].text}')
                    for data in datas:
                        box.add_widget(Builder.load_string(data))
                        adjust_height(box)
                        adjust_height(self.screen_manager.get_screen('main screen').ids.homescreen_manager.get_screen(
                            'get flights screen').ids.get_flights_outer_box)
                    self.homescreenchanger('home - flights')
                elif x != None:
                    self.show_notification(
                        x, 'home-tab-home', notifier=[obj[5], obj[6]])

            # User screen
            case 'user details':
                self.username = load_user_data()['username'].strip()
                x = UserDetails.UserDetails().validate(
                    obj[1:], obj[0], self.username)
                if x != None:
                    self.show_alert_dialog('user details', x)
                    if x == True:
                        update_user_data(
                            f'{obj[3].text.strip()[0].upper()}{obj[3].text.strip()[1:].lower()}')
                        Clock.schedule_once(self.fill_user_data, 5)
            case 'new email':
                self.username = load_user_data()['username'].strip()
                x = UserDetails.UserDetails().validateCode(obj, self.otp)
                if x == True:
                    UserDetails.UserDetails().update_email(
                        self.username, obj[2])
                    self.show_alert_dialog('new email', x)
                    self.fill_user_data()
                    Clock.schedule_once(
                        partial(self.userscreenchanger, 'email - home'), 5.5)
                    Clock.schedule_once(
                        partial(self.reset_screen, 'new email', obj), 5.5)
                elif x == False:
                    self.show_notification('Incorrect Code\nRetry', notifier=[
                                           self.userscreen_email.ids.new_email_notification_box, self.userscreen_email.ids.new_email_notification_text])

            case 'update password code':
                self.username = load_user_data()['username'].strip()
                x = UserDetails.UserDetails().validateCode(obj[1:], self.otp)
                if x == True:
                    obj[0].disabled = True
                    obj[1].disabled = True
                    obj[1].text = ''
                    obj[1].error = False
                    obj[2].disabled = True
                    obj[3].text = 'Code has been verified....Now you can update with your new password'
                    for one in obj[4:]:
                        one.disabled = False
                elif x == False:
                    self.show_notification('Incorrect Code\nRetry', notifier=[
                                           self.userscreen_password.ids.update_password_notification_box, self.userscreen_password.ids.update_password_notification_text])

            case 'update password':
                self.username = load_user_data()['username'].strip()
                x = UserDetails.UserDetails().check_password(
                    self.username, obj[1].text)
                self.show_alert_dialog('update password', x)

            case 'update wallet upi':
                x = UserWallet.UserWallet().validatePin(obj)
                if x == True:
                    UserWallet.UserWallet().update_amount(
                        self.username, obj[2].text.split('Rs ')[1])
                    self.fill_user_data()
                    self.show_alert_dialog()
                    Clock.schedule_once(partial(self.show_notification, 'Payment Successful', notifier=[
                                        self.userscreen_update_wallet_upi.ids.update_wallet_upi_notification_box, self.userscreen_update_wallet_upi.ids.update_wallet_upi_notification_text]), 3)
                    Clock.schedule_once(
                        partial(self.userscreenchanger, 'back - home'), 5.3)
                else:
                    Clock.schedule_once(partial(self.show_notification, 'UPI Pin is incorrect', notifier=[
                                        self.userscreen_update_wallet_upi.ids.update_wallet_upi_notification_box, self.userscreen_update_wallet_upi.ids.update_wallet_upi_notification_text]), 1)

    # Input text validation

    def strvalidator(self, form, type, field):
        global key_pressed, key_modifier
        if form == 'login':
            Login.LoginApp().validatetext(type, field)
        elif form == 'signup':
            Signup.Signup().validatetext(type, field[0])
            Signup.Signup().fields_checker(field[1:])
        elif form == 'pnr':
            PnrChecker.PnrChecker().validatePnr(field)
        elif form == 'forgot':
            if type == 'username':
                self.username = field[0].text
            Forgot.ForgotPass().validatetext(type, field)
        elif form == 'new password':
            Forgot.ForgotPass().validatetext(type, field)
        elif form == 'search flights':
            SearchFlight.Search().validate_text(field)
        elif form == 'user details':
            UserDetails.UserDetails().validateText(type, field)
        elif form == 'user wallet':
            UserWallet.UserWallet().textvalidator(type, field)

    # Text input updater

    def check_input(self, obj, form):
        if form == 'search flights':
            SearchFlight.Search().update_input(obj)

    # Close dialog box
    def closedialog(self, *args, **kwargs):
        self.dialog.dismiss()
        self.reset_dialog()

    def dialogtitle(self, *args, **kwargs):
        self.dialog.title = self.dialog.title + '.'

    def clock_run(self):
        Clock.schedule_interval(self.dialogtitle, .5)
        Clock.schedule_once(self.reset_dialog, 3)

    def reset_dialog(self, *args, **kwargs):
        Clock.unschedule(self.dialogtitle)

    # Dialog box show
    def show_alert_dialog(self, type='loading', arg=''):
        self.dialog = MDDialog(title='Loading')
        self.dialog.add_widget(Builder.load_file('./screens/loadingscreen.kv'))
        self.dialog.open()
        self.clock_run()
        anim = Animation(duration=2)
        anim.start(self.dialog)
        anim.bind(on_complete=self.closedialog)
        match type:
            case 'login':
                if arg == True:
                    self.fill_user_data()
                    right_box = self.screen_manager.get_screen(
                        'main screen').ids.homescreen_manager.get_screen('home screen').ids.home_top_right_box
                    userdata = load_user_data()
                    remove_children(right_box)
                    right_box.add_widget(
                        MDIcon(icon='account', size_hint_x=.1))
                    right_box.add_widget(
                        MDLabel(text=userdata['username'], adaptive_height=True))
                    self.show_notification('Login Successful')
                    self.homescreenchanger('home screen')
                else:
                    self.show_notification(
                        'Error, No such data not found.....Please retry')

            case 'signup':
                if arg == True:
                    self.show_notification(
                        'Success! You have created a new account\nPlease login to your account')
                    self.homescreenchanger('home screen')
                else:
                    self.show_notification(
                        'Cannot create account.\n Username or email already exists.\n Please login if you want to access your account')

            case 'forgot password':
                if arg == True:
                    self.show_notification('Confirmed code')
                    self.homescreenchanger('new password screen')
                else:
                    self.show_notification('Error, Please enter correct code')

            case 'pnr':
                pnr_details_box = self.screen_manager.get_screen(
                    'main screen').ids.homescreen_manager.get_screen('pnr screen').ids.pnr_details_box
                remove_children(pnr_details_box)

                if arg != []:
                    pnr_details_box.line_color = 'black'
                    pnr_details_box.add_widget(
                        MDLabel(text='Booking Details', halign='center', adaptive_height=True))
                    for x in arg:
                        box = MDBoxLayout(MDLabel(text=f'PNR : {x[1]}', halign='center', adaptive_height=True), MDLabel(text=f'PASSENGER NAME : {x[3]}', halign='center', adaptive_height=True), MDLabel(text=f'SEAT : {x[4]}', halign='center', adaptive_height=True), MDLabel(text=f'PRICE : Rs.{int(x[5])}', halign='center', adaptive_height=True), MDLabel(
                            text=f'BOOKING DATE  : {x[6]}', halign='center', adaptive_height=True), orientation='vertical', elevation=5, pos_hint={'center_x': .5, 'top': .6}, adaptive_height=True, size_hint_x=1, md_bg_color='lightgrey', radius=[10,], padding=10, spacing=10,)
                        pnr_details_box.add_widget(box)

                    self.show_notification('Details Found')
                else:
                    pnr_details_box.line_color = 'white'
                    self.show_notification(
                        'No such booking found, please retry')

            case 'new password':
                if arg == False:
                    self.show_notification(
                        'New password updated successfully\nPlease login')
                    self.homescreenchanger('new password - home')
                else:
                    self.show_notification('Password already exists')

            case 'user details':
                if arg == True:
                    Clock.schedule_once(partial(self.show_notification, 'Details updated successfully', notifier=[
                                        self.userscreen_details.ids.user_details_notification_box, self.userscreen_details.ids.user_details_notification_text]), 2.5)
                else:
                    Clock.schedule_once(partial(self.show_notification, arg, notifier=[
                                        self.userscreen_details.ids.user_details_notification_box, self.userscreen_details.ids.user_details_notification_text]), 2.5)

            case 'new email':
                if arg == True:
                    Clock.schedule_once(partial(self.show_notification, 'Email address updated successfully', notifier=[
                                        self.userscreen_email.ids.new_email_notification_box, self.userscreen_email.ids.new_email_notification_text]), 2.5)

            case 'update password':
                if arg == False:
                    Clock.schedule_once(partial(self.show_notification, 'New Password has been updated', notifier=[
                                        self.userscreen_password.ids.update_password_notification_box, self.userscreen_password.ids.update_password_notification_text]), 2.5)
                    Clock.schedule_once(
                        partial(self.userscreenchanger, 'back - home'), 5.5)
                    Clock.schedule_once(
                        partial(self.reset_screen, 'update password'), 5.7)
                else:
                    Clock.schedule_once(partial(self.show_notification, 'Password already exists', notifier=[
                                        self.userscreen_password.ids.update_password_notification_box, self.userscreen_password.ids.update_password_notification_text]), 2.5)

            case 'loading':
                pass

        self.dialog.open()

    # Status message notifier
    def show_notification(self, text, screen='', notifier=None, *args, **kwargs):
        if notifier == None:
            self.notification_text.text = text
            anim = Animation(duration=.2)
            anim += Animation(duration=.1,
                              pos_hint={'center_x': .5, 'y': .8}, opacity=1)
            anim += Animation(duration=3)
            anim += Animation(duration=.5,
                              pos_hint={'center_x': .5, 'y': 2}, opacity=0)
            anim.start(self.notification_box)
        else:
            self.notification_box = notifier[0]
            self.notification_text = notifier[1]
            self.notification_text.text = text
            anim = Animation(duration=.2)
            anim += Animation(duration=.1,
                              pos_hint={'center_x': .5, 'y': .8}, opacity=1)
            anim += Animation(duration=3)
            anim += Animation(duration=.5,
                              pos_hint={'center_x': .5, 'y': 2}, opacity=0)
            anim.start(self.notification_box)

    # Date dialog

    def check_valid_date(self, instance, date, *args, **kwargs):
        min = datetime.date.today()
        max = datetime.date(
            datetime.date.today().year + 1,
            datetime.date.today().month,
            datetime.date.today().day,)
        if date >= min and date <= max:
            self.save_date(date)
            self.date_dialog.dismiss()
        else:
            self.date_dialog.open()

    def save_date(self, date):
        day = ('0' + date.strftime("%d"))[-2:]
        mon = ('0' + date.strftime("%m"))[-2:]
        yr = date.strftime("%Y")
        string = f'{day} / {mon} / {yr}'
        self.screen_manager.get_screen('main screen').ids.homescreen_manager.get_screen(
            'home screen').ids.search_date_button.text = string
        self.screen_manager.get_screen('main screen').ids.homescreen_manager.get_screen(
            'get flights screen').ids.get_flights_date.text = 'ON : ' + string

    def open_date_dialog(self, obj):
        self.date_dialog = MDDatePicker(
            year=datetime.date.today().year,
            month=datetime.date.today().month,
            day=datetime.date.today().day,
            mode='picker',)
        self.date_dialog.bind(on_save=self.check_valid_date)
        self.date_dialog.open()

    # Drop-down menu
    def menu_action(self, action):
        if self.menu:
            if action == 'close':
                self.menu.dismiss()
            elif action == 'open':
                self.menu.open()

    def update_menu(self, obj):
        if obj == 'clicked':
            self.menu.dismiss()
        else:
            if self.menu != None:
                self.menu.dismiss()
                remove_children(self.menu)
            text = obj.text.strip()
            menu_items = self.get_menu_items(obj)
            if text != '' and menu_items != []:
                self.menu = MDDropdownMenu(
                    caller=obj,
                    width_mult=4,
                    ver_growth='down',
                    hor_growth='right',
                    position='center',
                    items=menu_items,
                    max_height=400)
                self.menu.open()

    def get_menu_items(self, obj):
        text = obj.text.strip()
        airports = load_airports_data()
        updated_list = []
        menu_items = []
        if len(text) > 0 and airports != []:
            for x in airports:
                # print(x)
                if text.lower() in x['name'].lower() or text.lower() in x['iata'].lower():
                    updated_list.append(x)
        else:
            updated_list = airports

        for x in updated_list[0:21]:
            menu_items.append({
                "text": x['iata'],
                "secondary_text": x['name'],
                "viewclass": "TwoLineListItem",
                "height": 80,
                "on_release": lambda x=x['iata']: self.set_input_text(obj, x),
            })

        # print(menu_items)
        return menu_items

    def set_input_text(self, obj, text):
        self.menu.dismiss()
        obj.text = text
        obj.focus = True
        self.menu.dismiss()
        remove_children(self.menu)
        obj.focus = True
        self.menu.dismiss()

    # Count updater
    def update_count(self, worker, obj, scaler):
        if scaler == 'incr':
            if int(obj.text) < 5:
                obj.text = f'{int(obj.text)+1}'
        elif scaler == 'decr':
            if int(obj.text) > 1:
                obj.text = f'{int(obj.text)-1}'

    # ------------------------------------------------------------------------------------------------------
    # Header-text animation for screens
    def text_anim(self, type, string='', *args, **kwargs):
        match type:
            case 'login':
                self.screen_manager.get_screen('main screen').ids.homescreen_manager.get_screen(
                    'login screen').ids.login_head.text = string
            case 'signup':
                self.screen_manager.get_screen('main screen').ids.homescreen_manager.get_screen(
                    'signup screen').ids.signup_head.text = string
            case 'flights':
                self.screen_manager.get_screen('main screen').ids.homescreen_manager.get_screen(
                    'get flights screen').ids.get_flights_query.text = 'FLIGHTS FOR : ' + string.upper()
            case 'update password email':
                if len(self.email.split('@')[0]) > 8:
                    self.userscreen_password.ids.update_password_email.text = f"Code sent to {self.email.split('@')[0][0:2]}XXX{self.email.split('@')[0][-2:]}@{self.email.split('@')[1]}"
                else:
                    self.userscreen_password.ids.update_password_email.text = f"Code sent to {self.email.split('@')[0][0]}XXX{self.email.split('@')[0][-1]}@{self.email.split('@')[1]}"
            case 'update wallet upi':
                self.userscreen_update_wallet_upi.ids.update_wallet_upi_amount.text = 'Rs ' + \
                    self.userscreen_update_wallet.ids.update_wallet_amount.text

    # Send code button

    def codebutton(self, btn, objs):
        objs[0].disabled = True
        # stores username in the class so as to use it to push the new password created to the particular record
        self.username = objs[0].text.strip()[0].upper() + \
            objs[0].text.strip()[1:].lower()
        self.otp = Forgot.ForgotPass().send_email(objs)
        revrange = list(range(0, 11))
        revrange.reverse()
        # print(revrange)
        for i in revrange:
            Clock.schedule_once(
                partial(self.codebutton_timer, btn, i), float(10 - i + .5))

    def codebutton_timer(self, obj, time, *args, **kwargs):
        if time == 0:
            obj.text = 'Send code'
            obj.disabled = False
        else:
            obj.disabled = True
            obj.text = f'Wait {time}s'


if __name__ == '__main__':
    MainApp().run()
