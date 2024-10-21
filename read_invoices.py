import re


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
            if email not in email_invoices:
                email_invoices[email] = []
            email_invoices[email].append(invoice_details)

    return email_invoices


# Usage example
file_name = 'invoices_data.txt'  # Replace with your actual file name
invoice_data = read_invoice_file(file_name)  # Read the file
invoices = extract_invoices(invoice_data)  # Extract invoices

# Print the extracted invoices
for email, invoice_list in invoices.items():
    print(f"Email: {email}")
    for invoice in invoice_list:
        print("Invoice Data:")
        print(invoice)  # No separator line between invoices
