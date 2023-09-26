import re, json, sqlite3

class UserWallet():
    def textvalidator(self, type, objs):
        amountreg = '[^0-9]'
        match type:
            case 'amount':
                objs[0].text = re.sub(amountreg, '', objs[0].text)
                if objs[0].text.strip() == '':
                    # objs[0].errors = True
                    objs[1].disabled = True
                elif re.sub('\D', '', objs[0].text.strip()) == '0':
                    objs[0].text = ''
                    objs[1].disabled = True
                elif int(objs[0].text.strip()) > 100000 :
                    objs[0].text = objs[0].text.strip()[0:-1]
                    # objs[1].disabled = True
                else:
                    objs[1].disabled = False
                    
                    

