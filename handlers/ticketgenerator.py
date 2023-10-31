from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors

# function to generate a ticket
def generate_flight_ticket(data):
    print(data)

    # Create a PDF file for the ticket
    c = canvas.Canvas("flight_ticket.pdf", pagesize=letter)

    # Set background color
    c.saveState()
    c.setFillColor(colors.lightblue)
    c.rect(0, 0, 612, 792, fill=1)
    c.restoreState()

    # Set font and font size for Title
    c.setFont("Helvetica", 20)
    c.setFillColor(colors.black)
    c.drawImage("./assets/airline.png", 50, 675, width=75, height=75)
    c.drawCentredString(300, 710, "Eagle Airline Pvt. Ltd.")
    c.setFont("Helvetica", 16)
    c.drawCentredString(300, 680, "Flight Ticket | E-copy")

    # Passenger Name
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, 630, "Passenger Name:")
    c.setFont("Helvetica", 12)
    temp_x = 200
    for name in data["passenger_name"]:
        c.drawString(temp_x, 630, name)
        temp_x = temp_x + 75

    # Flight Details
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, 610, "Flight Number:")
    c.setFont("Helvetica", 12)
    c.drawString(200, 610, str(data["flight_number"]))

    # PNR 
    c.setFont("Helvetica-Bold", 12)
    c.drawString(250, 610, "PNR Number:")
    c.setFont("Helvetica", 12)
    c.drawString(340, 610, data["pnr_number"])

    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, 590, "Departure Airport:")
    c.setFont("Helvetica", 12)
    c.drawString(200, 590, data["departure_city"])

    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, 570, "Arrival Airport:")
    c.setFont("Helvetica", 12)
    c.drawString(200, 570, data["arrival_city"])

    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, 550, "Departure Date & Time:")
    c.setFont("Helvetica", 12)
    c.drawString(200, 550, str(data["departure_date_time"]))

    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, 530, "Arrival Date & Time:")
    c.setFont("Helvetica", 12)
    c.drawString(200, 530, str(data['arrival_date_time']))

    # Ticket Price
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, 510, "Ticket Price:")
    c.setFont("Helvetica-Bold", 12)
    c.setFillColor(colors.red)
    priceText = "Rs. " + str(data['ticket_price'])
    c.drawString(200, 510, priceText)

    # Footer
    c.setFont("Helvetica", 10)
    c.setFillColor(colors.black)

    footer_text = [
        "Terms & Conditions:",
        "1. The ticket is non-transferable.",
        "2. Boarding gates close 30 minutes before departure.",
        "3. Baggage must adhere to size and weight restrictions.",
        "4. Changes or cancellations may incur fees.",
        "5. Mobile or printed ticket must be presented at security and boarding.",
        "NOTE: This PDF is for reference. Please use the official Eagle Airline app for boarding.",
    ]

    y_position = 150
    for line in footer_text:
        c.drawString(50, y_position, line)
        y_position -= 20

    # Save the PDF file
    print("Data Maked")
    c.showPage()
    c.save()

    print("Flight ticket PDF generated as flight_ticket.pdf")
