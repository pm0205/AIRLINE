from handlers.ticketgenerator import generate_flight_ticket
import sqlite3
import shutil
import os

# Define ticket details needed for PDF
dataRequire = {
    "passenger_name": "",
    "flight_number": "",
    "departure_city": "",
    "arrival_city": "",
    "departure_date_time": "",
    "arrival_date_time": "",
    "ticket_price": "",
    "pnr_number": ""
}

# get all passengers details from DB
def check_passengers(passengers):
    passengers_details = []
    conn = sqlite3.connect('./data/database.db')
    c = conn.cursor()
    for x in passengers:
        c.execute('SELECT * FROM tickets WHERE ticket_id = (:id)', {
            'id': x
        })
        record = c.fetchone()
        passengers_details.append(record)
    if passengers_details != []:
        passengers_names = []
        for x in passengers_details:
            passengers_names.append(x[3])
        
        return passengers_names
    else:
        return None

# copy the files into download folder
def getFileToDownload():
    source_file = './flight_ticket.pdf'
    destination_directory = os.path.expanduser('~\\Downloads')

    # Create the destination path by combining the destination directory and the filename
    destination_file = os.path.join(destination_directory, os.path.basename(source_file))
    
    # Copy the file to the destination
    shutil.copy(source_file, destination_file)

    print(f"'{os.path.basename(source_file)}' copied to the Downloads folder.")

# function for fetching all details required for printing PDF
def fetch_ticket_data_for_pdf(booking):
    passengers = check_passengers(booking["passengers"])
    dataRequire["flight_number"] = booking["id"]
    dataRequire["passenger_name"] = passengers
    dataRequire["departure_city"] = booking["source"]
    dataRequire["arrival_city"] = booking["destination"]
    dataRequire["departure_date_time"] = booking["departure"]
    dataRequire["arrival_date_time"] = booking["arrival"]
    dataRequire["pnr_number"] = booking["pnr"]
    dataRequire["ticket_price"] = len(passengers) * 2700
    
    # Call the function to generate the flight ticket
    generate_flight_ticket(dataRequire)

    # get the file to downloads folder
    getFileToDownload()
