from fpdf import FPDF


def save_invoices_as_pdf(email_invoices):
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

    # Add invoice details
    for line in invoice_details.split('\n'):
        pdf.cell(200, 10, line, ln=True, align='L')

    pdf_file_name = f"invoice_{invoice_number}.pdf"
    pdf.output(pdf_file_name)
    return pdf_file_name
