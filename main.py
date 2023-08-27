from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel, MDIcon
from kivymd.uix.button import MDRaisedButton
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder
import scripts.login as Login
import scripts.pnrChecker as PnrChecker
import json

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

class MainApp(MDApp):
    dialog = None
    def load_all_files(self):
        self.screen_manager.get_screen('main screen').ids.homescreen_manager.add_widget(Builder.load_file('./screens/homescreen.kv'))
        self.screen_manager.get_screen('main screen').ids.homescreen_manager.add_widget(Builder.load_file('./screens/pnrscreen.kv'))
        self.screen_manager.get_screen('main screen').ids.homescreen_manager.add_widget(Builder.load_file('./screens/loginscreen.kv'))
        userdata = load_user_data()
        if check_saved_data() == True:
            remove_children(self.screen_manager.get_screen('main screen').ids.homescreen_manager.get_screen('home screen').ids.home_top_right_box)
            self.screen_manager.get_screen('main screen').ids.homescreen_manager.get_screen('home screen').ids.home_top_right_box.add_widget(MDIcon(icon='account', size_hint_x = .1))
            self.screen_manager.get_screen('main screen').ids.homescreen_manager.get_screen('home screen').ids.home_top_right_box.add_widget(MDLabel(text=userdata['username'], adaptive_height=True))
            self.homescreenchanger('home screen')


    def build(self):
        self.theme_cls.theme_style = 'Light'  # or 'Dark'
        self.theme_cls.primary_palette = 'Blue'
        
        self.screen_manager = ScreenManager()
        self.screen_manager.add_widget(Builder.load_file('main_screen.kv'))
        self.load_all_files()
        return self.screen_manager
    
    def homescreenchanger(self, screen_name):
        match screen_name:
            case 'pnr screen': 
                self.screen_manager.get_screen('main screen').ids.homescreen_manager.current = 'pnr screen'
                self.screen_manager.get_screen('main screen').ids.homescreen_manager.transition.direction = 'left'
            case 'login screen': 
                self.screen_manager.get_screen('main screen').ids.homescreen_manager.current = 'login screen'
                self.screen_manager.get_screen('main screen').ids.homescreen_manager.transition.direction = 'down'
            case 'home screen': 
                self.screen_manager.get_screen('main screen').ids.homescreen_manager.current = 'home screen'
                self.screen_manager.get_screen('main screen').ids.homescreen_manager.transition.direction = 'right'

    def validate(self, type, obj):
        match type:
            case 'login':
                x = Login.LoginApp().validateLogin(obj[0], obj[1], obj[2])
                if x == True:
                    self.show_alert_dialog('login', x)
                elif x == False:
                    self.show_alert_dialog('login', x)
                else:
                    pass
            case 'pnr':
                x = PnrChecker.PnrChecker().validatePnr(obj)
                if x != False:
                    self.show_alert_dialog('pnr', x)
    
    def strvalidator(self, form, type, field):
        if form == 'login':
            Login.LoginApp().validatetext(type, field)
        elif form == 'pnr':
            PnrChecker.PnrChecker().validatePnr(field)

    def closedialog(self, obj):
        self.dialog.dismiss()
    
    def show_alert_dialog(self, type, arg):
        match type:
            case 'login':
                if arg == True:
                    dialogtitle = 'Success'
                    self.dialog = MDDialog(title = dialogtitle, buttons=[MDRaisedButton(text="OK", on_release = self.closedialog),],)
                    userdata = load_user_data()
                    remove_children(self.screen_manager.get_screen('main screen').ids.homescreen_manager.get_screen('home screen').ids.home_top_right_box)
                    self.screen_manager.get_screen('main screen').ids.homescreen_manager.get_screen('home screen').ids.home_top_right_box.add_widget(MDIcon(icon='account', size_hint_x = .1))
                    self.screen_manager.get_screen('main screen').ids.homescreen_manager.get_screen('home screen').ids.home_top_right_box.add_widget(MDLabel(text=userdata['username'], adaptive_height=True))
                    self.homescreenchanger('home screen')
                else:
                    dialogtitle = 'Error'
                    self.dialog = MDDialog(title = dialogtitle, text = 'Data not found.....Please retry', buttons=[MDRaisedButton(text="OK", on_release = self.closedialog),],)

            case 'pnr': 
                if arg != []:
                    dialogtitle = 'Booking Details'
                    self.dialog = MDDialog(title = dialogtitle, text=f'     PNR : {arg[0]}\n\n     SEAT : {arg[1]}\n\n     FLIGHT STATUS : {arg[2]}', buttons=[MDRaisedButton(text="OK", on_release = self.closedialog),],)
                else:
                    dialogtitle = 'No Booking Found'
                    self.dialog = MDDialog(title = dialogtitle, text=f'Please retry', buttons=[MDRaisedButton(text="OK", on_release = self.closedialog),],)





        self.dialog.open()

if __name__ == '__main__':
    MainApp().run()
