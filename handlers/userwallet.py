import re, json, sqlite3, time

class UserWallet():
    def update_amount(self, username, amount):
        conn = sqlite3.connect('./data/database.db')
        c = conn.cursor()
        c.execute('SELECT wallet from users WHERE username = (:username)', {
            'username': username.strip()[0].upper() + username.strip()[1:].lower()
        })
        prev_amount = c.fetchone()[0]
        # print(amount)
        time.sleep(.5)
        c.execute('UPDATE users SET wallet = (:wallet) WHERE username = (:username)', {
            'username': username.strip()[0].upper() + username.strip()[1:].lower(),
            'wallet': int(prev_amount) + int(amount)
        })
        conn.commit()
        conn.close()

    def validatePin(self, objs):
        if objs[1].text.strip()=='123456':
            return True
        else:
            return False

    def textvalidator(self, type, objs):
        numreg = '[^0-9]'
        match type:
            case 'amount':
                objs[0].text = re.sub(numreg, '', objs[0].text)
                if objs[0].text.strip() == '':
                    objs[1].disabled = True
                elif re.sub('\D', '', objs[0].text.strip()) == '0':
                    objs[0].text = ''
                    objs[1].disabled = True
                elif int(objs[0].text.strip()) > 100000 :
                    objs[0].text = objs[0].text.strip()[0:-1]
                else:
                    objs[1].disabled = False
                    
            case 'pin':
                objs[0].text = re.sub(numreg, '', objs[0].text)
                if objs[0].text.strip() == '':
                    objs[1].disabled = True
                elif len(objs[0].text.strip()) < 6 :
                    objs[1].disabled = True
                elif len(objs[0].text.strip()) == 6 :
                    objs[1].disabled = False
                elif len(objs[0].text.strip()) > 6 :
                    objs[0].text = objs[0].text.strip()[0:-1]
                    
                    

