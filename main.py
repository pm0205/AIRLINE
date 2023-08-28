from kivymd.app import MDApp
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager
from kivymd.uix.dialog import MDDialog
from kivy.animation import Animation
from kivymd.uix.label import MDLabel, MDIcon
from kivymd.uix.button import MDRectangleFlatButton, MDFlatButton, MDRaisedButton
from kivy.lang import Builder
import handlers.login as Login
import handlers.pnrChecker as PnrChecker
import json, time

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
    
def remove_children(obj):
    children = [child for child in obj.children]
    for child in children:
        obj.remove_widget(child)

# Main APP code starts here ................
class MainApp(MDApp):
    dialog = None

    # pre-load all screens 
    def load_all_files(self):
        self.screen_manager.get_screen('main screen').ids.homescreen_manager.add_widget(Builder.load_file('./screens/homescreen.kv'))
        self.screen_manager.get_screen('main screen').ids.homescreen_manager.add_widget(Builder.load_file('./screens/pnrscreen.kv'))
        self.screen_manager.get_screen('main screen').ids.homescreen_manager.add_widget(Builder.load_file('./screens/loginscreen.kv'))
        self.screen_manager.get_screen('main screen').ids.homescreen_manager.add_widget(Builder.load_file('./screens/signupscreen.kv'))
        self.screen_manager.get_screen('main screen').ids.homescreen_manager.add_widget(Builder.load_file('./screens/loadingscreen.kv'))

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
        self.screen_manager = ScreenManager()
        self.screen_manager.add_widget(Builder.load_file('./screens/windowscreen.kv'))
        self.load_all_files()
        self.notification_box = self.screen_manager.get_screen('main screen').ids.notification_box
        self.notification_text = self.screen_manager.get_screen('main screen').ids.notification_text
        return self.screen_manager
    
    def on_start(self):
        self.show_alert_dialog('loading', '')

    def homescreenchanger(self, screen_name):
        match screen_name:
            case 'pnr screen': 
                self.screen_manager.get_screen('main screen').ids.homescreen_manager.current = 'pnr screen'
                self.screen_manager.get_screen('main screen').ids.homescreen_manager.transition.direction = 'left'
            case 'login screen': 
                self.screen_manager.get_screen('main screen').ids.homescreen_manager.current = 'login screen'
                self.screen_manager.get_screen('main screen').ids.homescreen_manager.transition.direction = 'down'
            case 'signup screen': 
                self.screen_manager.get_screen('main screen').ids.homescreen_manager.current = 'signup screen'
                self.screen_manager.get_screen('main screen').ids.homescreen_manager.transition.direction = 'down'
            case 'login-signup': 
                self.screen_manager.get_screen('main screen').ids.homescreen_manager.current = 'signup screen'
                self.screen_manager.get_screen('main screen').ids.homescreen_manager.transition.direction = 'left'
            case 'home screen': 
                self.screen_manager.get_screen('main screen').ids.homescreen_manager.current = 'home screen'
                self.screen_manager.get_screen('main screen').ids.homescreen_manager.transition.direction = 'right'

    # Input validation when button is clicked
    def validate(self, type, obj):
        match type:
            case 'login':
                x = Login.LoginApp().validateLogin(obj[0], obj[1], obj[2])
                if (x == True) or (x == False):
                    self.show_alert_dialog('login', x)
                else:
                    pass
            case 'pnr':
                x = PnrChecker.PnrChecker().validatePnr(obj)
                if x != False:
                    # self.show_alert_dialog('loading', '')
                    self.show_alert_dialog('pnr', x)
    
    # Input text validation
    def strvalidator(self, form, type, field):
        if form == 'login':
            Login.LoginApp().validatetext(type, field)
        elif form == 'pnr':
            PnrChecker.PnrChecker().validatePnr(field)

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
        anim = Animation(duration=3)
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

            case 'pnr': 
                pnr_details_box = self.screen_manager.get_screen('main screen').ids.homescreen_manager.get_screen('pnr screen').ids.pnr_details_box
                remove_children(pnr_details_box)

                if arg != []:
                    pnr_details_box.line_color = 'black'
                    pnr_details_box.add_widget(MDLabel(text = 'Booking Details', halign = 'center', adaptive_height = True))
                    pnr_details_box.add_widget(MDLabel(text = f'PNR : {arg[0]}', halign = 'center', adaptive_height = True))
                    pnr_details_box.add_widget(MDLabel(text = f'SEAT : {arg[1]}', halign = 'center', adaptive_height = True))
                    pnr_details_box.add_widget(MDLabel(text = f'FLIGHT STATUS : {arg[2]}', halign = 'center', adaptive_height = True))
                    self.show_notification('Details Found')
                else:
                    pnr_details_box.line_color = 'white'
                    self.show_notification('No such booking found, please retry')
            
            case 'loading':
                pass
       
        self.dialog.open()
    
    # Status message notifier
    def show_notification(self, text):
        self.notification_text.text = text
        anim = Animation(duration=3)
        anim += Animation(duration=.1, pos_hint = {'center_x':.5, 'y': .8}, opacity = 1)
        anim += Animation(duration=2)
        anim += Animation(duration=.5, pos_hint = {'center_x':.5, 'y': 2}, opacity = 0)
        anim.start(self.notification_box)

if __name__ == '__main__':
    MainApp().run()
