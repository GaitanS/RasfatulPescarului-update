# Răsfățul Pescarului

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/downloads/release/python-3120/)
[![Django](https://img.shields.io/badge/Django-5.1.5-green.svg)](https://www.djangoproject.com/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple.svg)](https://getbootstrap.com/)

Răsfățul Pescarului is a comprehensive online platform for fishing enthusiasts in Romania. The project combines an e-commerce system with interactive fishing location maps, video tutorials, and a solunar calendar to provide a complete fishing experience.

## Features

### 🎣 Fishing Locations
- Interactive map with fishing spots across Romania
- Detailed location information (facilities, rules, prices)
- Filtering by county and region
- User reviews and ratings

### 🛒 E-commerce
- Product catalog with categories and filters
- Shopping cart functionality
- Secure checkout process
- Multiple payment methods (Stripe, bank transfer)
- Order tracking and history

### 📹 Video Tutorials
- Fishing techniques and tips
- Categorized video content
- Embedded video player
- Expert fishing advice

### 🌙 Solunar Calendar
- Daily fishing predictions
- Moon phase tracking
- Best fishing times
- Location-based calculations

### 👤 User Features
- Secure authentication system
- Email verification
- Password reset functionality
- User profiles
- Order history

## Technology Stack

### Backend
- Python 3.12
- Django 5.1.5
- Django REST Framework
- Celery for async tasks
- Redis for caching

### Frontend
- Bootstrap 5.3
- Font Awesome icons
- JavaScript/jQuery
- Leaflet.js for maps

### Database & Storage
- SQLite (development)
- PostgreSQL (production ready)
- Django Storages for media files

### Services
- Stripe for payment processing
- Google reCAPTCHA
- SMTP email service
- Solunar calculations (Astral)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/RasfatulPescarului.git
cd RasfatulPescarului
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/macOS
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a .env file in the project root with the following variables:
```
SECRET_KEY=your_secret_key
STRIPE_PUBLIC_KEY=your_stripe_public_key
STRIPE_SECRET_KEY=your_stripe_secret_key
STRIPE_WEBHOOK_SECRET=your_stripe_webhook_secret
RECAPTCHA_PUBLIC_KEY=your_recaptcha_public_key
RECAPTCHA_PRIVATE_KEY=your_recaptcha_private_key
EMAIL_HOST_USER=your_email
EMAIL_HOST_PASSWORD=your_email_password
```

5. Run migrations:
```bash
python manage.py migrate
```

6. Create a superuser:
```bash
python manage.py createsuperuser
```

7. Start the development server:
```bash
python manage.py runserver
```

## Configuration

### Email Setup
The project uses SMTP for email notifications. Configure your email settings in settings.py or .env file:
```python
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
```

### Payment Integration
Stripe is used for payment processing. Set up your Stripe keys in the .env file:
```
STRIPE_PUBLIC_KEY=your_stripe_public_key
STRIPE_SECRET_KEY=your_stripe_secret_key
STRIPE_WEBHOOK_SECRET=your_stripe_webhook_secret
```

### Security
- reCAPTCHA protection for forms
- CSRF protection enabled
- Secure password hashing
- Email verification required
- Session security settings

## Production Deployment

1. Set DEBUG=False in settings.py
2. Configure PostgreSQL database
3. Set up static files serving with whitenoise
4. Configure proper email backend
5. Set up proper domain in ALLOWED_HOSTS
6. Configure SSL/HTTPS
7. Set up proper media storage

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, email contact@rasfatulpescarului.ro or create an issue in the repository.
