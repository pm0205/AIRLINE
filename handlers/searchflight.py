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

    def validate_text(obj):
        pass