from fpdf import FPDF


def save_invoices_as_pdf(email_invoices):  # Try to use templates 
    # Generates PDFs for each invoice
    email_pdf_mapping = {}

    for email, invoice_list in email_invoices.items():
        pdf_files = []
        for invoice_number, invoice_details in invoice_list:
            pdf_file = _helper_invoice_as_pdf(invoice_number, invoice_details)
            pdf_files.append(pdf_file)
        email_pdf_mapping[email] = pdf_files

    return email_pdf_mapping


def _helper_invoice_as_pdf(invoice_number, invoice_details):
    # Generate a PDF from the invoice details
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Logo
    pdf.image("company_logo.jpg", 10, 8, 33)
    pdf.set_font("Arial", "B", 16)
    pdf.set_xy(8, 35)
    pdf.cell(0, 10, "Comapny Inc.", ln=True,)
    # pdf.ln(20)

    #Header
    pdf.set_font("Arial", 'B', 16)
    pdf.set_y(0)
    pdf.cell(200, 10, f"Invoice #{invoice_number}", ln=True, align='C')
    pdf.ln(50) # Empty lines

    # Add invoice details
    for line in invoice_details.split('\n'):
        if "products" in line:
            pdf.set_font("Arial", 'B', 12)
        elif "Total" in line:
            pdf.set_font("Arial", 'BU', 14)
        else:
            pdf.set_font("Arial",'I', 12)
        pdf.cell(0, 10, line, ln=True, align='L', border=1)
    
    # Footer
    pdf.ln(10)
    pdf.set_font("Arial", 'I', 12)
    pdf.set_text_color(62,73,80)
    pdf.cell(0, 10, "Thank you for your business!", ln=True, align='C')

    pdf_file_name = f"invoice_{invoice_number}.pdf"
    pdf.output(pdf_file_name)
    return pdf_file_name
