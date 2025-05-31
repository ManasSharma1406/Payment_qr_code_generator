# QR Code Generator for UPI Payments

This Django application allows users to generate QR codes for UPI payments using PhonePe, Google Pay, and Paytm. The application features a black and white themed frontend and stores the generated QR codes in a history section.

## Detailed Code Explanation

### 1. Models (`qr_app/models.py`)
The `QRCodeHistory` model is the core of our data storage system:

```python
class QRCodeHistory(models.Model):
    upi_id = models.CharField(max_length=255)  # Stores the UPI ID
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=100.00)  # Payment amount
    message = models.CharField(max_length=255, default='Payment')  # Optional payment message
    phonepe_qr = models.ImageField(upload_to='qr_codes/')  # Stores PhonePe QR code image
    gpay_qr = models.ImageField(upload_to='qr_codes/')  # Stores Google Pay QR code image
    paytm_qr = models.ImageField(upload_to='qr_codes/')  # Stores Paytm QR code image
    created_at = models.DateTimeField(default=timezone.now)  # Timestamp of creation
```

### 2. Views (`qr_app/views.py`)
The application has two main views:

#### Generate QR View
```python
def generate_qr(request):
    if request.method == 'POST':
        # Get form data
        upi_id = request.POST.get('upi_id')
        amount = request.POST.get('amount', '100')
        message = request.POST.get('message', 'Payment')

        # Generate UPI URLs for different payment apps
        phonepe_url = f"upi://pay?pa={upi_id}&pn={upi_id}&am={amount}&tn={message}"
        gpay_url = f"upi://pay?pa={upi_id}&pn={upi_id}&am={amount}&tn={message}"
        paytm_url = f"upi://pay?pa={upi_id}&pn={upi_id}&am={amount}&tn={message}"

        # Create QR codes using qrcode library
        phonepe_qr = qrcode.make(phonepe_url)
        gpay_qr = qrcode.make(gpay_url)
        paytm_qr = qrcode.make(paytm_url)

        # Save QR codes to database
        qr_history = QRCodeHistory(
            upi_id=upi_id,
            amount=amount,
            message=message
        )
        # Save QR code images
        qr_history.save()
```

#### History View
```python
class QRCodeHistoryView(ListView):
    model = QRCodeHistory
    template_name = 'qr_app/history.html'
    context_object_name = 'qr_codes'
    ordering = ['-created_at']  # Show newest first
```

### 3. Templates

#### Base Template (`base.html`)
The base template provides the common structure and styling:
- Black and white theme
- Responsive navigation
- Common CSS styles
- Container structure

#### Generate Template (`generate.html`)
Contains the form for generating QR codes:
- UPI ID input field
- Amount input field
- Message input field
- Submit button

#### History Template (`history.html`)
Displays the history of generated QR codes:
- List of all generated QR codes
- QR code images for each payment app
- Details like UPI ID, amount, and timestamp

### 4. URL Configuration (`qr_app/urls.py`)
```python
urlpatterns = [
    path('', views.generate_qr, name='generate'),
    path('history/', views.QRCodeHistoryView.as_view(), name='history'),
]
```

### 5. Settings Configuration (`qr_generator/settings.py`)
Key settings include:
- Media file configuration for storing QR code images
- Database configuration
- Installed apps list
- Static and media file settings

## Features

- Generate QR codes for UPI payments.
- Support for PhonePe, Google Pay, and Paytm.
- Black and white themed user interface.
- History section to view previously generated QR codes.
- Responsive design for all devices.
- Secure file handling for QR code images.

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Virtual environment (recommended)

## Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment:**
   - On Windows:
     ```bash
     .\venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

2. **Access the application:**
   Open your web browser and go to `http://127.0.0.1:8000/`.

3. **Generate a QR Code:**
   - Enter your UPI ID (e.g., example@upi)
   - Enter the amount (default: ₹100)
   - Add an optional message
   - Click "Generate QR Code"

4. **View History:**
   - Click on "History" in the navigation bar
   - View all previously generated QR codes
   - Each entry shows:
     - UPI ID
     - Amount
     - Message
     - Generation timestamp
     - QR codes for all three payment apps

## Project Structure

```
qr_generator/
├── manage.py
├── qr_generator/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── qr_app/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── templates/
│       └── qr_app/
│           ├── base.html
│           ├── generate.html
│           └── history.html
├── media/
│   └── qr_codes/
├── static/
└── requirements.txt
```

## Deployment

To deploy this application to a live server, follow these general steps:

1. **Choose a Hosting Provider:**
   - **Platform as a Service (PaaS):** Heroku, PythonAnywhere, Render, Railway
   - **Virtual Private Server (VPS):** DigitalOcean, AWS (EC2), Google Cloud (Compute Engine), Linode

2. **Set up the Production Environment:**
   - Install Python, Django, and other dependencies
   - Set up a production database (e.g., PostgreSQL, MySQL)
   - Configure static and media file serving

3. **Configure Django Settings:**
   - Set `DEBUG = False`
   - Update `ALLOWED_HOSTS` with your server's domain name or IP address
   - Configure the production database settings
   - Set `STATIC_ROOT` and `MEDIA_ROOT` paths

4. **Use a Production Web Server and Application Server:**
   - Use Nginx or Apache as the web server
   - Use Gunicorn or uWSGI as the application server

5. **Run Migrations:**
   ```bash
   python manage.py migrate
   ```

6. **Collect Static Files:**
   ```bash
   python manage.py collectstatic
   ```

7. **Manage Processes:**
   - Use a process manager like Systemd or Supervisor to keep the application server running

## Security Considerations

1. **File Storage:**
   - QR code images are stored securely in the media directory
   - File names are unique to prevent conflicts
   - Media files are served through Django's media handling

2. **Data Validation:**
   - Input validation for UPI ID format
   - Amount validation to prevent invalid values
   - CSRF protection for all forms

3. **Production Security:**
   - Debug mode disabled in production
   - Secure secret key management
   - Proper file permissions

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Django for the web framework
- qrcode and Pillow for QR code generation and image handling
- Contributors and maintainers of all used libraries 