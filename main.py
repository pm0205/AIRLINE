from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel, MDIcon
from kivymd.uix.button import MDRectangleFlatButton, MDFlatButton, MDRaisedButton
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder
import login as Login
import json

def check_saved_data():
    f = open('./userdata.json')
    data = json.load(f)
    f.close()
    return data['saved']

def load_user_data():
    f = open('./userdata.json')
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
        self.screen_manager.add_widget(Builder.load_file('windowscreen.kv'))
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
                    self.show_alert_dialog(x)
                elif x == False:
                    self.show_alert_dialog(x)
                else:
                    pass
    
    def strvalidator(self, form, fields):
        if form == 'login':
            Login.LoginApp().validatetext(fields[0], fields[1])

    def closedialog(self, obj):
        self.dialog.dismiss()
    
    def show_alert_dialog(self, status):
        if status == True:
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
        self.dialog.open()

if __name__ == '__main__':
    MainApp().run()
    
