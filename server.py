# server.py

from flask import Flask, request, jsonify, render_template, send_from_directory
import os
from werkzeug.utils import secure_filename
from read_invoices import read_invoice_file, extract_invoices
from pdf_generator import save_invoices_as_pdf
from mailing import send_email

class InvoiceServer:
    def __init__(self):
        # Initialize Flask app with template directory
        self.app = Flask(__name__, 
                        template_folder='templates',
                        static_folder='static')
        self.configure_app()
        self.setup_routes()

    def configure_app(self):
        # Configure upload settings
        self.UPLOAD_FOLDER = 'uploads'
        self.ALLOWED_EXTENSIONS = {'txt'}
        self.app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB max file size
        self.app.config['UPLOAD_FOLDER'] = self.UPLOAD_FOLDER

        # Create necessary directories if they don't exist
        for directory in ['uploads', 'templates', 'static']:
            if not os.path.exists(directory):
                os.makedirs(directory)

    def allowed_file(self, filename):
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in self.ALLOWED_EXTENSIONS

    def setup_routes(self):
        @self.app.route('/')
        def home():
            return render_template('index.html')

        @self.app.route('/upload', methods=['POST'])
        def upload_file():
            return self.handle_upload()

        @self.app.errorhandler(404)
        def page_not_found(e):
            return jsonify({
                'success': False,
                'error': 'Resource not found'
            }), 404

        @self.app.errorhandler(413)
        def request_entity_too_large(error):
            return jsonify({
                'success': False,
                'error': 'File too large. Maximum size is 5MB'
            }), 413

    def handle_upload(self):
        try:
            # Check if file is present in request
            if 'file' not in request.files:
                return jsonify({
                    'success': False,
                    'error': 'No file provided'
                }), 400

            file = request.files['file']

            # Check if file was actually selected
            if file.filename == '':
                return jsonify({
                    'success': False,
                    'error': 'No file selected'
                }), 400

            # Validate file type
            if not self.allowed_file(file.filename):
                return jsonify({
                    'success': False,
                    'error': 'Invalid file type. Only .txt files are allowed'
                }), 400

            # Save file securely
            filename = secure_filename(file.filename)
            filepath = os.path.join(self.app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            try:
                # Process the file
                invoice_data = read_invoice_file(filepath)
                extracted_invoices = extract_invoices(invoice_data)

                if not extracted_invoices:
                    raise ValueError("No valid invoices found in the file")

                # Generate PDFs
                invoice_pdfs = save_invoices_as_pdf(extracted_invoices)

                # Send emails
                email_results = []
                for email, invoices in invoice_pdfs.items():
                    receiver = email
                    attachment = invoices
                    subject = "Your Invoices"
                    body = "Hi User, Please check the attached invoices"

                    send_email(receiver, subject, body, attachment)
                return jsonify({
                    'success': True,
                    'message': f'Successfully processed {len(extracted_invoices)} invoices',
                    'details': {
                        'total_invoices': len(extracted_invoices),
                        'email_results': email_results
                    }
                })

            except Exception as e:
                print("error:", e)
                return jsonify({
                    'success': False,
                    'error': f'Error processing invoices: {str(e)}'
                }), 500

            finally:
                # Clean up - remove uploaded file
                if os.path.exists(filepath):
                    os.remove(filepath)

        except Exception as e:
            return jsonify({
                'success': False,
                'error': f'Server error: {str(e)}'
            }), 500

    def run(self, host='0.0.0.0', port=5000, debug=False):
        self.app.run(host=host, port=port, debug=debug)


# Run the server if this file is executed directly
if __name__ == '__main__':
    server = InvoiceServer()
    server.run(debug=True)