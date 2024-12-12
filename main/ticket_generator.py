from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

def generate_ticket_pdf(ticket_data, output_path="ticket.pdf"):
    c = canvas.Canvas(output_path, pagesize=letter)
    width, height = letter

    c.setFont("Helvetica-Bold", 16)
    c.drawString(200, height - 50, "Cinema Ticket")

    c.setFont("Helvetica", 12)
    y_position = height - 100
    line_height = 20

    for key, value in ticket_data.items():
        c.drawString(50, y_position, f"{key}: {value}")
        y_position -= line_height

    c.setFont("Helvetica-Oblique", 10)
    c.drawString(50, 50, "Thank you for using CinemaTicket!")

    c.save()
    print(f"Ticket saved to {output_path}")

if __name__ == "__main__":
    ticket_info = {
        "Customer Name": "John Doe",
        "Movie": "Interstellar",
        "Cinema": "Azadi Cinema",
        "Hall": "3",
        "Seat": "Row 5, Seat 10",
        "Show Time": "2024-12-15 18:30",
        "Price": "500,000 IRR"
    }
    generate_ticket_pdf(ticket_info, output_path="ticket.pdf")
