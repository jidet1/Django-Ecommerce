# Django E-commerce Application with Flutterwave Payment Integration

This is a full-featured e-commerce web application built with Django. It supports product browsing, cart management, user authentication, order processing, and payment integration using Flutterwave.

---

## Features

- User registration and login
- Product listing and detailed views
- Shopping cart management (for logged-in and guest users)
- Order placement and tracking
- Admin dashboard for managing orders and shipping statuses
- Integration with Flutterwave payment gateway (test mode)
- Secure payment verification and order status updates

---

## Demo

Check out the live demo here:  
[https://django-ecommerce-production-3a9c.up.railway.app/](https://django-ecommerce-production-3a9c.up.railway.app/)

---

## Getting Started

### Prerequisites

- Python 3.8+
- Django 4.x
- Flutterwave API credentials (test mode)

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/jidet1/Django-Ecommerce.git
   cd Django-Ecommerce
   
2. Create and activate a virtual environment:

    ```bash
    python -m venv env
    source env/bin/activate  # On Windows: env\Scripts\activate


3. Install dependencies:

    ```bash
    pip install -r requirements.txt


4. Set up your environment variables for Flutterwave API keys in .env or directly in settings.py:

    ```bash
    FLUTTERWAVE_PUBLIC_KEY = 'your_flutterwave_public_key'
    FLUTTERWAVE_SECRET_KEY = 'your_flutterwave_secret_key'

5. Apply migrations:
    ```bash
    python manage.py migrate

6. python manage.py migrate
    ```bash
    python manage.py runserver


**Payment Testing**
The app uses Flutterwave's test mode for payments. You can test the payment process using Flutterwave’s test cards available here:
Flutterwave Test Cards

**Project Structure**
payment/ - Payment app including order and payment handling
store/ - Product listing and catalog management
templates/ - HTML templates for front-end rendering
static/ - Static assets (CSS, JS, images)


**Known Issues & Future Improvements**
Improve UI/UX for mobile responsiveness
Add email notifications for order confirmation and shipping updates
Enhance security for payment callbacks and webhook handling
Implement real-time stock management


**License**
This project is open-source and available under the MIT License.


**Contact**
Feel free to reach out if you want to contribute or have questions!
GitHub: https://github.com/jidet1/Django-Ecommerce



