# Răsfățul Pescarului

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/downloads/release/python-3120/)
[![Django](https://img.shields.io/badge/Django-5.1.5-green.svg)](https://www.djangoproject.com/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple.svg)](https://getbootstrap.com/)

Răsfățul Pescarului is a comprehensive platform for fishing enthusiasts in Romania, providing interactive fishing location maps, video tutorials, and a solunar calendar to enhance your fishing experience.

## Features

### 🎣 Fishing Locations
- Interactive map with fishing spots across Romania
- Detailed location information including facilities and rules
- Filtering by county and region
- User reviews and ratings

### 📹 Video Tutorials
- Comprehensive fishing tutorials
- Tips and techniques for different fishing styles
- Seasonal fishing guides

### 🌙 Solunar Calendar
- Daily fishing predictions
- Moon phase tracking
- Best fishing times calculator

## Technology Stack

- Python 3.12
- Django 5.1.5
- Bootstrap 5.3
- PostgreSQL
- Redis

## Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/RasfatulPescarului.git
cd RasfatulPescarului
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables in .env file:
```
DEBUG=True
SECRET_KEY=your_secret_key
DATABASE_URL=your_database_url
REDIS_URL=your_redis_url
```

5. Run migrations:
```bash
python manage.py migrate
```

6. Start the development server:
```bash
python manage.py runserver
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
