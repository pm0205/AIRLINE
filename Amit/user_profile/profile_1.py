from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivymd.uix.screenmanager import ScreenManager
from kivy.core.text import LabelBase
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFloatingActionButton
from kivymd.uix.floatlayout import MDFloatLayout

class My(MDApp):
    def build (self):
            
             screen_manager = ScreenManager()

             screen_manager.add_widget(Builder.load_file('profile.kv'))

             return screen_manager
    
My().run()
