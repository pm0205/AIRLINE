from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
import sqlite3, re

class PnrChecker:
    def validatePnr(self, obj):
        inputBox = obj[0]
        pnr_number = inputBox.text
        special_char = re.compile('[^a-zA-Z\d\s:]')

        # check user_input PNR
        if(len(pnr_number)==0):
            inputBox.error = True
            inputBox.helper_text = 'Required'
        elif (special_char.search(pnr_number)!=None):
            inputBox.error = True
            inputBox.helper_text = 'PNR can only contain alphanumeric characters'
        elif not re.match("^[a-zA-Z0-9]+$", pnr_number):
            inputBox.error = True
            inputBox.helper_text = 'PNR contains spaces in between'
        elif(len(pnr_number) != 6):
            inputBox.error = True
            inputBox.helper_text = 'PNR must be 6 characters only'
        else:
            if obj[1]:
                data = self.check_database_for_pnr(pnr_number)
                if data != []:
                    data = data[0]
                    obj[2].text = f"PNR Number: {data[0]} \nSeat No.: {data[1]} \nFlight Status: {data[2]}"
                else:
                    obj[2].text = "Invalid PNR number, Please check again."

            return True

        return False

    def check_database_for_pnr(self, pnr_number):
        conn = sqlite3.connect("credential.db")
        
        # create cursor for cmds
        c = conn.cursor()

        # execute cmd for credentials table
        c.execute("SELECT * FROM ticketsInfo WHERE PNR = (:pnr)", {
            "pnr": pnr_number
        })
        record = c.fetchall()

        # commit and close 
        conn.commit()
        conn.close()

        return record

if __name__ == "__main__":
    PnrChecker().run()
