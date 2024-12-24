from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
import io

def generate_ticket_pdf(request):
    ticket_data = {
        "Name": request.GET.get("name", "N/A"),
        "Family": request.GET.get("family", "N/A"),
        "Number of Tickets": request.GET.get("num_tickets", "N/A"),
        "Seats": request.GET.get("seats", "N/A"),
        "Cinema": request.GET.get("cinema", "N/A"),
        "Movie": request.GET.get("movie", "N/A"),
    }

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)

    styles = getSampleStyleSheet()
    title_style = styles["Title"]
    title_style.textColor = colors.HexColor("#FF0000")

    header_style = styles["Heading2"]
    header_style.textColor = colors.HexColor("#333333")
    header_style.alignment = 1  # Center alignment

    text_style = styles["BodyText"]
    text_style.fontSize = 12

    elements = []
    title = Paragraph("🎟 Cinema Ticket 🎟", title_style)
    elements.append(title)
    elements.append(Spacer(1, 20))

    table_data = [
        ["Field", "Details"],  # Header row
        ["Name", ticket_data["Name"]],
        ["Family", ticket_data["Family"]],
        ["Number of Tickets", ticket_data["Number of Tickets"]],
        ["Seats", ticket_data["Seats"]],
        ["Cinema", ticket_data["Cinema"]],
        ["Movie", ticket_data["Movie"]],
    ]

    table = Table(table_data, colWidths=[150, 300])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#FF0000")),  # Header row background
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),  # Header row text color
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 12),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
        ("BACKGROUND", (0, 1), (-1, -1), colors.whitesmoke),
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
    ]))

    elements.append(table)
    elements.append(Spacer(1, 30))

    footer = Paragraph(
        "Thank you for using <b>CinemaTicket</b>! Enjoy the movie. 🎬",
        text_style
    )
    elements.append(footer)

    doc.build(elements)
    buffer.seek(0)

    response = HttpResponse(buffer, content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="ticket.pdf"'
    return response
