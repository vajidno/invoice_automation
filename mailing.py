import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import os
# Fixed sender email
SENDER_EMAIL = "adityanaresh007@gmail.com" #Use the Sender email
PASSWORD = "mcxx rsps sgfm giqy"  # Use App Password if 2FA is enabled

def send_email(receiver_email, subject, body, attachments=None):
    server = None  # Initialize server to None
    try:
        # Create a multipart message
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = receiver_email
        msg['Subject'] = subject

        # Add email body
        msg.attach(MIMEText(body, 'plain'))

        # Handle multiple attachments
        if attachments:
            for filename in attachments:
                if os.path.isfile(filename):
                    with open(filename, 'rb') as f:
                        part = MIMEApplication(f.read(), Name=filename)
                        part['Content-Disposition'] = f'attachment; filename="{filename}"'
                        msg.attach(part)
                else:
                    print(f"Attachment '{filename}' not found in the root folder.")

        # Connect to the SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  # Secure the connection
        server.login(SENDER_EMAIL, PASSWORD)  # Log in

        # Send the email
        server.sendmail(SENDER_EMAIL, receiver_email, msg.as_string())
        print("Email sent successfully!")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        if server:
            server.quit()  # Close the connection



