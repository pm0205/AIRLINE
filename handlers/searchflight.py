import re, json
class Search():
    
    def check_flight_codes(self, code):
        f = open('./data/airports.json')
        flag = False
        data = json.load(f)
        data = [x for x in data if x['type'] == 'airport']
        for x in data :
            if code.lower() == x['iata'].lower():
                flag = True
        return flag

    def update_input(self, obj):
        letters = re.compile('[a-zA-Z]')
        new = ''
        for x in obj.text.strip():
            if letters.search(x) != None:
                new += x
        obj.text = new

    def validate(self, objs):
        if self.validate_text(objs[1]) == True and self.validate_text(objs[2]) == True:
            if objs[3].text.strip() != 'Choose Date':
                if self.check_flight_codes(objs[1].text.strip()) and self.check_flight_codes(objs[2].text.strip()):
                    if objs[1].text.strip() != objs[2].text.strip():
                        return True
                    else : 
                        return 'From and To locations cannot be the same'
                else:
                    return 'No such Airports found......Please update and try again'
            else:
                return 'Choose date'
        else: 
            return None

    def validate_text(self, obj):
        text = obj.text.strip()
        flag = False
        if len(text) == 0:
            obj.error = True
            obj.helper_text = 'Required'
            flag = False
        elif len(text) > 3:
            obj.error = True
            obj.helper_text = 'Only 3 characters code-name allowed'
            flag = False
        else: 
            obj.error = False
            flag = True
        return flag