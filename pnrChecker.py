from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
import sqlite3, re

class PnrChecker:
    def validatePnr(self, obj):
        pnr_number = obj.text
        special_char = re.compile('[^a-zA-Z\d\s:]')

        # check user_input PNR
        if(len(pnr_number)==0):
            obj.error = True
            obj.helper_text = 'Required'
        elif (special_char.search(pnr_number)!=None):
            obj.error = True
            obj.helper_text = 'PNR can only contain alphanumeric characters'
        elif not re.match("^[a-zA-Z0-9]+$", pnr_number):
            obj.error = True
            obj.helper_text = 'PNR contains spaces in between'
        elif(len(pnr_number) != 6):
            obj.error = True
            obj.helper_text = 'PNR must be 6 characters only'
        else:
            return True

        return False

if __name__ == "__main__":
    PnrChecker().run()
