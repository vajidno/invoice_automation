import re
from pdf_generator import save_invoices_as_pdf
from mailing import send_email

def read_invoice_file(file_name):
    # Read the invoice data from the specified file.
    with open(file_name, 'r') as file:
        data = file.read()
    return data

def extract_invoices(data):
    # Extract email and associated invoice data from the given text.
    # Define a pattern to match email addresses
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'

    # Initialize a dictionary to hold email and corresponding invoice data
    email_invoices = {}
    invoice_numbers_by_email = {}

    # Use finditer to locate all email matches in the text
    for email_match in re.finditer(email_pattern, data):
        email = email_match.group(0)

        # Find the start of the current invoice by locating the email position
        start_pos = email_match.end()

        # Define a pattern to match the subsequent invoice details
        invoice_pattern = r'(?P<invoice_details>.*?)(?=\n{1,}Customer Email|Email|$)'

        # Search for invoice details starting from the email position
        invoice_details_match = re.search(invoice_pattern, data[start_pos:], re.DOTALL)

        if invoice_details_match:
            # Extract invoice details and clean up the text
            invoice_details = invoice_details_match.group('invoice_details').strip()

            # Extract Invoice Number to detect duplicates
            invoice_number_match = re.search(r'Invoice Number:\s*(\S+)', invoice_details)

            if invoice_number_match:
                invoice_number = invoice_number_match.group(1)

                # Initialize email if not already in the dictionary
                if email not in email_invoices:
                    email_invoices[email] = []
                    invoice_numbers_by_email[email] = set()

                # Check if the invoice number is already present using the set
                if invoice_number not in invoice_numbers_by_email[email]:
                    date = re.search(r'Date:\s*(\S+)', invoice_details).group(1)
                    items = re.findall(r'Item:\s*(.+)', invoice_details)
                    split_items = [item.split(",")[0] for item in items]
                    print(split_items)
                    price = re.findall(r'Price:\s*(\S+)', invoice_details)
                    print("prices:", price)
                    quantity = re.findall(r'Quantity:\s*(\d+)', invoice_details)
                    print("quantities:", quantity)
                    name = email
                    email_invoices[email].append((invoice_number, date,split_items,price,quantity,name))
                    invoice_numbers_by_email[email].add(invoice_number)  # Add the invoice number to the set

    return email_invoices

# Usage example
# file_name = 'invoices_data.txt'  # Replace with your actual file name
# invoice_data = read_invoice_file(file_name)  # Read the file
# extracted_invoices = extract_invoices(invoice_data)  # Extract invoices

# # # Generate PDFs from extracted invoices
# invoice_pdfs = save_invoices_as_pdf(extracted_invoices)

# print(invoice_pdfs)

# # Iterate through the invoice_pdfs and call the mail function

# for email, invoices in invoice_pdfs.items():
#     # Need to get the username from the mail
#     receiver = email
#     attachment = invoices
#     subject = "Invoices"
#     body = "Hi user , Please check the attached invoices"

#     send_email(receiver, subject, body, attachment)


