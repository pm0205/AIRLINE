import sqlite3, json, datetime, ast
conn = sqlite3.connect("./data/database.db")
c = conn.cursor()
# # c.execute(f"SELECT * FROM users where username = (:username)", {'username' : 'Alkaison'})
# c.execute("ALTER TABLE users RENAME COLUMN id_user to user_id")
# c.execute("ALTER TABLE users RENAME COLUMN name_user to name")
# c.execute("ALTER TABLE users RENAME COLUMN mail_user to mail")
# c.execute("ALTER TABLE users RENAME COLUMN phone_user to phone")
# c.execute("ALTER TABLE users ADD COLUMN wallet integer")
# conn.commit()
# conn.close()
# f = open('./data/airports.json')
# c.execute('UPDATE users SET username = "Admin1" WHERE password = "Admin123"')
# c.execute('UPDATE users SET wallet = 0 WHERE wallet < 1 OR wallet IS null')

# fromdate = datetime.datetime(year = 2023, month = 11, day = 12, hour = 7)
# todate = datetime.datetime(year = 2023, month = 11, day = 12, hour = 10)
# c.execute('UPDATE flights SET departure_time = (:date) WHERE flight_number = "AI101"', {
#     'date': fromdate.strftime('%d/%m/%Y %H:%M:%S')
# })
# c.execute('UPDATE flights SET arrival_time = (:date) WHERE flight_number = "AI101"', {
#     'date': todate.strftime('%d/%m/%Y %H:%M:%S')
# })

# c.execute('SELECT wallet from users WHERE username = (:username)', {
#             'username': 'Admin'
#         })
# amount = c.fetchone()
# print(amount[0])
c.execute('SELECT bookings from users WHERE username = (:username)', {
            'username': 'Admin'
        })
record= c.fetchone()
fromdate = datetime.datetime(year = 2023, month = 11, day = 5, hour = 23)
todate = datetime.datetime(year = 2023, month = 11, day = 6, hour = 1)
duration = ((todate - fromdate).days*24) + ((todate - fromdate).seconds/3600)
# bookings = [{"id": 20, "source": "DEL", "destination": "BOM",  "departure": fromdate.strftime('%d/%m/%Y %H:%M:%S'), "arrival": todate.strftime('%d/%m/%Y %H:%M:%S'), "duration": duration , "pnr": "SHA128", "passengers": [1, 4], "cancelled": False}, 
# {"id": 28, "source": "BOM", "destination": "BLR",  "departure": "23/10/2023 09:00:00", "arrival": "23/10/2023 12:00:00", "duration": 3 , "pnr": "FGJ098", "passengers": [3], "cancelled": False}]
booking = {"id": 34, "source": "BOM", "destination": "DEL",  "departure": fromdate.strftime('%d/%m/%Y %H:%M:%S'), "arrival": todate.strftime('%d/%m/%Y %H:%M:%S'), "duration": duration , "pnr": "SCJ294", "passengers": [1, 4], "cancelled": False}
bookings = json.loads(record[0])
# bookings.append(booking)
# c.execute('UPDATE users SET bookings = (:bookings) WHERE username = "Admin"', {
#             'bookings': json.dumps(bookings)
#         })
for booking in bookings:
    print(booking)
conn.commit()
conn.close()
