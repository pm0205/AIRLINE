from kivymd.app import MDApp
from kivy.clock import Clock
from kivy.lang import Builder
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
    FakeRectangularElevationBehavior,
    BackgroundColorBehavior)
from kivy.uix.behaviors import ButtonBehavior
import handlers.login as Login
import handlers.pnrChecker as PnrChecker
import handlers.forgot as Forgot
import handlers.signup as Signup
import handlers.searchflight as SearchFlight
import json, time, datetime
from functools import partial

def check_saved_data():
    f = open('./data/userdata.json')
    data = json.load(f)
    f.close()
    return data['saved']

def load_user_data():
    f = open('./data/userdata.json')
    data = json.load(f)
    f.close()
    return data

def load_airports_data():
    f = open('./data/airports.json')
    data = json.load(f)
    data = [x for x in data if x['type'] == 'airport' and x['name'] != None]
    f.close()
    return data

def remove_children(obj):
    children = [child for child in obj.children]
    for child in children:
        obj.remove_widget(child)

# Build components
class DialogContent(MDFloatLayout):
    pass

class NotificationBox(FakeRectangularElevationBehavior, MDBoxLayout):
    pass

class Box3d(FakeRectangularElevationBehavior,
    MDBoxLayout):
    pass

class ElevButton(FakeRectangularElevationBehavior, MDFillRoundFlatButton):
    pass

# Main APP code starts here ................
class MainApp(MDApp):
    dialog = None
    menu = None

    # pre-load all screens 
    def load_all_files(self):
        self.screen_manager.get_screen('main screen').ids.homescreen_manager.add_widget(Builder.load_file('./screens/homescreen.kv'))
        self.screen_manager.get_screen('main screen').ids.homescreen_manager.add_widget(Builder.load_file('./screens/pnrscreen.kv'))
        self.screen_manager.get_screen('main screen').ids.homescreen_manager.add_widget(Builder.load_file('./screens/loginscreen.kv'))
        self.screen_manager.get_screen('main screen').ids.homescreen_manager.add_widget(Builder.load_file('./screens/signupscreen.kv'))
        # self.screen_manager.get_screen('main screen').ids.homescreen_manager.add_widget(Builder.load_file('./screens/loadingscreen.kv'))
        self.screen_manager.get_screen('main screen').ids.homescreen_manager.add_widget(Builder.load_file('./screens/forgotpasswordscreen.kv'))
        self.screen_manager.get_screen('main screen').ids.homescreen_manager.add_widget(Builder.load_file('./screens/newpasswordscreen.kv'))

        # Check if login was details were saved to auto-login
        userdata = load_user_data()
        if check_saved_data() == True:
            remove_children(self.screen_manager.get_screen('main screen').ids.homescreen_manager.get_screen('home screen').ids.home_top_right_box)
            self.screen_manager.get_screen('main screen').ids.homescreen_manager.get_screen('home screen').ids.home_top_right_box.add_widget(MDIcon(icon='account', size_hint_x = .1))
            self.screen_manager.get_screen('main screen').ids.homescreen_manager.get_screen('home screen').ids.home_top_right_box.add_widget(MDLabel(text=userdata['username'],halign='center', adaptive_height=True))
            self.homescreenchanger('home screen')

    def build(self):
        self.theme_cls.theme_style = 'Light'  # or 'Dark'
        self.theme_cls.primary_palette = 'Blue'
        self.icon = "./assets/icon.ico"
        self.screen_manager = ScreenManager()
        self.screen_manager.add_widget(Builder.load_file('./screens/windowscreen.kv'))
        self.load_all_files()
        self.notification_box = self.screen_manager.get_screen('main screen').ids.notification_box
        self.notification_text = self.screen_manager.get_screen('main screen').ids.notification_text
        return self.screen_manager
    
    def on_start(self):
        self.title = "Eagle Airline | Ticket Booking System"
        self.show_alert_dialog('loading', '')

    def homescreenchanger(self, screen_name):
        match screen_name:
            case 'pnr screen': 
                self.screen_manager.get_screen('main screen').ids.homescreen_manager.current = 'pnr screen'
                self.screen_manager.get_screen('main screen').ids.homescreen_manager.transition.direction = 'left'
            case 'login screen': 
                self.screen_manager.get_screen('main screen').ids.homescreen_manager.current = 'login screen'
                self.screen_manager.get_screen('main screen').ids.homescreen_manager.transition.direction = 'down'
                Clock.schedule_once(partial(self.text_anim, 'login', 'L'), 0.5)
                Clock.schedule_once(partial(self.text_anim, 'login', 'LO'), 1)
                Clock.schedule_once(partial(self.text_anim, 'login', 'LOG'), 1.5)
                Clock.schedule_once(partial(self.text_anim, 'login', 'LOGI'), 2)
                Clock.schedule_once(partial(self.text_anim, 'login', 'LOGIN'), 2.5)
            case 'signup screen': 
                self.screen_manager.get_screen('main screen').ids.homescreen_manager.current = 'signup screen'
                self.screen_manager.get_screen('main screen').ids.homescreen_manager.transition.direction = 'down'
                Clock.schedule_once(partial(self.text_anim, 'signup', 'S'), 0.5)
                Clock.schedule_once(partial(self.text_anim, 'signup', 'SI'), 1)
                Clock.schedule_once(partial(self.text_anim, 'signup', 'SIG'), 1.5)
                Clock.schedule_once(partial(self.text_anim, 'signup', 'SIGN'), 2)
                Clock.schedule_once(partial(self.text_anim, 'signup', 'SIGN '), 2.5)
                Clock.schedule_once(partial(self.text_anim, 'signup', 'SIGN U'), 3)
                Clock.schedule_once(partial(self.text_anim, 'signup', 'SIGN UP'), 3.5)
            case 'login-signup': 
                self.screen_manager.get_screen('main screen').ids.homescreen_manager.current = 'signup screen'
                self.screen_manager.get_screen('main screen').ids.homescreen_manager.transition.direction = 'left'
            case 'home screen': 
                self.screen_manager.get_screen('main screen').ids.homescreen_manager.current = 'home screen'
                self.screen_manager.get_screen('main screen').ids.homescreen_manager.transition.direction = 'right'
            case 'forgot screen': 
                # reseting all elements
                self.screen_manager.get_screen('main screen').ids.homescreen_manager.get_screen('forgotpassword screen').ids.forgotusername.disabled = False
                self.screen_manager.get_screen('main screen').ids.homescreen_manager.get_screen('forgotpassword screen').ids.forgotusername.text = ''
                self.screen_manager.get_screen('main screen').ids.homescreen_manager.get_screen('forgotpassword screen').ids.code_field.disabled = True
                self.screen_manager.get_screen('main screen').ids.homescreen_manager.get_screen('forgotpassword screen').ids.code_field.text = ''
                self.screen_manager.get_screen('main screen').ids.homescreen_manager.get_screen('forgotpassword screen').ids.sendcode_button.disabled = True
                self.screen_manager.get_screen('main screen').ids.homescreen_manager.get_screen('forgotpassword screen').ids.confirmcode_btn.disabled = True
                # transition of screen
                self.screen_manager.get_screen('main screen').ids.homescreen_manager.current = 'forgotpassword screen'
                self.screen_manager.get_screen('main screen').ids.homescreen_manager.transition.direction = 'up'
            case 'new password screen':
                # reset widgets
                self.screen_manager.get_screen('main screen').ids.homescreen_manager.get_screen('new password screen').ids.new_password1.text = ''
                self.screen_manager.get_screen('main screen').ids.homescreen_manager.get_screen('new password screen').ids.new_password2.text = ''
                self.screen_manager.get_screen('main screen').ids.homescreen_manager.get_screen('new password screen').ids.confirmpassword_btn.disabled = True
                # screen transition
                self.screen_manager.get_screen('main screen').ids.homescreen_manager.current = 'new password screen'
                self.screen_manager.get_screen('main screen').ids.homescreen_manager.transition.direction = 'left'
            case 'new password - home':
                # reset widgets
                self.screen_manager.get_screen('main screen').ids.homescreen_manager.get_screen('new password screen').ids.new_password1.text = ''
                self.screen_manager.get_screen('main screen').ids.homescreen_manager.get_screen('new password screen').ids.new_password2.text = ''
                self.screen_manager.get_screen('main screen').ids.homescreen_manager.get_screen('new password screen').ids.confirmpassword_btn.disabled = True
                # screen transition
                self.screen_manager.get_screen('main screen').ids.homescreen_manager.current = 'home screen'
                self.screen_manager.get_screen('main screen').ids.homescreen_manager.transition.direction = 'up'

    # Input validation when button is clicked
    def validate(self, type, obj):
        match type:
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
                x = Forgot.ForgotPass().validateCode(obj[0], obj[1], self.otp)
                if (x == True) or (x == False):
                    self.show_alert_dialog('forgot password', x)
                else: 
                    pass
            case 'confirm password':
                x = Forgot.ForgotPass().check_password(self.username, obj[1].text)
                self.show_alert_dialog('new password', x)
            case 'search flights':
                x = SearchFlight.Search().validate(obj)
                if x != True:
                    self.show_notification(x, 'home-tab-home', notifier=[obj[5], obj[6]])
    
    # Input text validation
    def strvalidator(self, form, type, field):
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
    def show_alert_dialog(self, type, arg):
        self.dialog = MDDialog(title = 'Loading')
        self.dialog.add_widget(Builder.load_file('./screens/loadingscreen.kv'))
        self.dialog.open()
        self.clock_run()
        anim = Animation(duration=2)
        anim.start(self.dialog)
        anim.bind(on_complete=self.closedialog)
        match type:
            case 'login':
                if arg == True:
                    right_box = self.screen_manager.get_screen('main screen').ids.homescreen_manager.get_screen('home screen').ids.home_top_right_box
                    userdata = load_user_data()
                    remove_children(right_box)
                    right_box.add_widget(MDIcon(icon='account', size_hint_x = .1))
                    right_box.add_widget(MDLabel(text=userdata['username'], adaptive_height=True))
                    self.show_notification('Login Successful')
                    self.homescreenchanger('home screen')
                else:
                    self.show_notification('Error, No such data not found.....Please retry')
                    
            case 'signup':
                if arg == True: 
                    self.show_notification('Success! You have created a new account\nPlease login to your account')
                    self.homescreenchanger('home screen')
                else:
                    self.show_notification('Cannot create account.\n Username or email already exists.\n Please login if you want to access your account')

            case 'forgot password':
                if arg == True:
                    self.show_notification('Confirmed code')
                    self.homescreenchanger('new password screen')
                else:
                    self.show_notification('Error, Please enter correct code')

            case 'pnr': 
                pnr_details_box = self.screen_manager.get_screen('main screen').ids.homescreen_manager.get_screen('pnr screen').ids.pnr_details_box
                remove_children(pnr_details_box)

                if arg != []:
                    pnr_details_box.line_color = 'black'
                    pnr_details_box.add_widget(MDLabel(text = 'Booking Details', halign = 'center', adaptive_height = True))
                    for x in arg:
                        box = MDBoxLayout(MDLabel(text = f'PNR : {x[1]}', halign = 'center', adaptive_height = True), MDLabel(text = f'PASSENGER NAME : {x[3]}', halign = 'center', adaptive_height = True), MDLabel(text = f'SEAT : {x[4]}', halign = 'center', adaptive_height = True), MDLabel(text = f'PRICE : Rs.{int(x[5])}', halign = 'center', adaptive_height = True),MDLabel(text = f'BOOKING DATE  : {x[6]}', halign = 'center', adaptive_height = True), orientation = 'vertical', elevation= 5, pos_hint = {'center_x':.5, 'top': .6}, adaptive_height = True, size_hint_x = 1 ,md_bg_color =  'lightgrey', radius = [10,], padding = 10, spacing = 10,)
                        pnr_details_box.add_widget(box)

                    self.show_notification('Details Found')
                else:
                    pnr_details_box.line_color = 'white'
                    self.show_notification('No such booking found, please retry')
            
            case 'new password':
                if arg == False:
                    self.show_notification('New password updated successfully\nPlease login')
                    self.homescreenchanger('new password - home')
                else:
                    self.show_notification('Password already exists')

            case 'loading':
                pass
       
        self.dialog.open()
    
    # Status message notifier
    def show_notification(self, text, screen = '', notifier = None):
        if screen == '':
            self.notification_text.text = text
            anim = Animation(duration=3)
            anim += Animation(duration=.1, pos_hint = {'center_x':.5, 'y': .8}, opacity = 1)
            anim += Animation(duration=2)
            anim += Animation(duration=.5, pos_hint = {'center_x':.5, 'y': 2}, opacity = 0)
            anim.start(self.notification_box)
        elif screen == 'home-tab-home':
            self.notification_box = notifier[0]
            self.notification_text = notifier[1]
            self.notification_text.text = text
            anim = Animation(duration=.2)
            anim += Animation(duration=.1, pos_hint = {'center_x':.5, 'y': .8}, opacity = 1)
            anim += Animation(duration=2)
            anim += Animation(duration=.5, pos_hint = {'center_x':.5, 'y': 2}, opacity = 0)
            anim.start(self.notification_box)
    
    # Date dialog
    def check_valid_date(self, instance, date, *args, **kwargs):
        min = datetime.date.today()
        max = datetime.date(
            datetime.date.today().year + 1,
            datetime.date.today().month,
            datetime.date.today().day,)
        if date>=min and date<=max:
            self.save_date(date)
            self.date_dialog.dismiss()
        else:
            self.date_dialog.open()

    def save_date(self, date):
        string = date.strftime("%d / %m / %y")
        self.screen_manager.get_screen('main screen').ids.homescreen_manager.get_screen('home screen').ids.search_date_button.text = string

    def open_date_dialog(self, obj):
        self.date_dialog = MDDatePicker(
            year = datetime.date.today().year,
            month = datetime.date.today().month,
            day = datetime.date.today().day,
            mode = 'picker',)
        self.date_dialog.bind(on_save = self.check_valid_date)
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
            if self.menu!=None:
                remove_children(self.menu)
            text = obj.text.strip()
            menu_items = self.get_menu_items(obj)
            if text != '' and menu_items != []:
                self.menu = MDDropdownMenu(
                    caller=obj,
                    width_mult=4,
                    ver_growth = 'down',
                    hor_growth = 'right',
                    position = 'center',
                    items = menu_items,
                    max_height = 400)
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
                    "on_release": lambda x = x['iata'] : self.set_input_text(obj, x) ,
                })
            
        print(menu_items)
        return menu_items
    
    def set_input_text(self, obj, text):
        self.menu.dismiss()
        obj.text = text

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
    def text_anim(self, type, string, *args, **kwargs):
        match type:
            case 'login':
                self.screen_manager.get_screen('main screen').ids.homescreen_manager.get_screen('login screen').ids.login_head.text = string
            case 'signup':
                self.screen_manager.get_screen('main screen').ids.homescreen_manager.get_screen('signup screen').ids.signup_head.text = string
    
    # Send code button
    def codebutton(self, btn, objs):
        objs[0].disabled = True
        # stores username in the class so as to use it to push the new password created to the particular record
        self.username = objs[0].text.strip()
        self.otp = Forgot.ForgotPass().send_email(objs)
        revrange = list(range(0, 11))
        revrange.reverse()
        # print(revrange)
        for i in revrange:
            Clock.schedule_once(partial(self.codebutton_timer, btn, i), float(10 - i + .5))

    def codebutton_timer(self, obj, time, *args, **kwargs):
        if time == 0:
            obj.text = 'Send code'
            obj.disabled = False
        else: 
            obj.disabled = True
            obj.text = f'Wait {time}s'

            

if __name__ == '__main__':
    MainApp().run()
