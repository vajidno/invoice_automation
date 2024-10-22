from fpdf import FPDF
from weasyprint import HTML
from flask import render_template

def save_invoices_as_pdf(email_invoices):  # Try to use templates 
    # Generates PDFs for each invoice
    email_pdf_mapping = {}

    for email, invoice_list in email_invoices.items():
        pdf_files = []
        print(f"{email} : {invoice_list}")
        for invoice_number, date, split_items, price, quantity, name in invoice_list:
            pdf_file = _helper_invoice_as_pdf(invoice_number, date, split_items, price, quantity, email)
            pdf_files.append(pdf_file)
        email_pdf_mapping[email] = pdf_files

    return email_pdf_mapping

def _helper_invoice_as_pdf(invoice_number, date, split_items, price, quantity, email):
    total = sum([float(p[1:]) * float(q) for p, q in zip(price, quantity)])

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Company Logo and Header
    pdf.image("company_logo.jpg", 10, 8, 33)
    pdf.set_font("Arial", "B", 18)
    pdf.set_xy(70, 15)
    pdf.cell(80, 10, "Company Inc.", align="C")
    pdf.ln(20)

    # Invoice Header Section
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, f"Invoice Number: {invoice_number}", ln=True, align='C')
    pdf.cell(200, 10, f"Date: {date}", ln=True, align='C')
    pdf.cell(200, 10, f"Customer: {email}", ln=True, align='C')
    pdf.ln(20)

    # Table Header for Items
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(60, 10, "Item", 1, 0, 'C')
    pdf.cell(40, 10, "Quantity", 1, 0, 'C')
    pdf.cell(40, 10, "Price", 1, 0, 'C')
    pdf.cell(40, 10, "Total", 1, 1, 'C')

    # Table Content
    pdf.set_font("Arial", size=12)
    for item, qty, prc in zip(split_items, quantity, price):
        item_total = float(prc[1:]) * float(qty)
        pdf.cell(60, 10, item, 1)
        pdf.cell(40, 10, qty, 1, 0, 'C')
        pdf.cell(40, 10, prc, 1, 0, 'C')
        pdf.cell(40, 10, f"${item_total:.2f}", 1, 1, 'C')

    # Total Amount Section
    pdf.ln(10)
    pdf.set_font("Arial", 'BU', 12)
    pdf.cell(180, 10, f"Grand Total: ${total:.2f}", align='R')

    # Footer Section
    pdf.ln(20)
    pdf.set_font("Arial", 'I', 12)
    pdf.set_text_color(62, 73, 80)
    pdf.cell(0, 10, "Thank you for your business!", ln=True, align='C')

    # Save PDF File
    pdf_file_name = f"invoice_{invoice_number}.pdf"
    pdf.output(pdf_file_name)
    return pdf_file_name