#!/bin/bash

# Deployment script for Răsfățul Pescarului on Hostinger
# Run this script on your Hostinger server

set -e  # Exit on any error

echo "🚀 Starting deployment for Răsfățul Pescarului..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
PROJECT_NAME="RasfatulPescarului"
DOMAIN="rasfatul-pescarului.ro"
REPO_URL="https://github.com/GaitanS/RasfatulPescarului-update.git"
PROJECT_DIR="/home/u123456789/domains/$DOMAIN/public_html"
VENV_DIR="/home/u123456789/virtualenv/$DOMAIN"

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running as correct user
if [ "$USER" != "u123456789" ]; then
    print_warning "Please run this script as your Hostinger user (u123456789)"
fi

# Update system packages
print_status "Updating system packages..."
# Note: On shared hosting, you might not have sudo access
# sudo apt update && sudo apt upgrade -y

# Create project directory if it doesn't exist
print_status "Creating project directory..."
mkdir -p "$PROJECT_DIR"
cd "$PROJECT_DIR"

# Clone or update repository
if [ -d ".git" ]; then
    print_status "Updating existing repository..."
    git pull origin main
else
    print_status "Cloning repository..."
    git clone "$REPO_URL" .
fi

# Create virtual environment if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
    print_status "Creating virtual environment..."
    python3 -m venv "$VENV_DIR"
fi

# Activate virtual environment
print_status "Activating virtual environment..."
source "$VENV_DIR/bin/activate"

# Upgrade pip
print_status "Upgrading pip..."
pip install --upgrade pip

# Install requirements
print_status "Installing Python dependencies..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    print_warning ".env file not found. Creating from example..."
    cp .env.example .env
    print_warning "Please edit .env file with your actual configuration!"
fi

# Load environment variables
if [ -f ".env" ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

# Collect static files
print_status "Collecting static files..."
python manage.py collectstatic --noinput

# Compress static files
print_status "Compressing static files..."
python manage.py compress --force

# Run database migrations
print_status "Running database migrations..."
python manage.py migrate

# Create superuser if needed (interactive)
print_status "Checking for superuser..."
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(is_superuser=True).exists():
    print('No superuser found. Please create one manually with: python manage.py createsuperuser')
"

# Set proper permissions
print_status "Setting file permissions..."
find "$PROJECT_DIR" -type f -exec chmod 644 {} \;
find "$PROJECT_DIR" -type d -exec chmod 755 {} \;
chmod +x "$PROJECT_DIR/manage.py"

# Create necessary directories
print_status "Creating necessary directories..."
mkdir -p "$PROJECT_DIR/media/uploads"
mkdir -p "$PROJECT_DIR/static"
mkdir -p "$PROJECT_DIR/logs"

print_status "✅ Deployment completed successfully!"
print_warning "Don't forget to:"
print_warning "1. Configure your .env file with actual values"
print_warning "2. Set up your database in Hostinger control panel"
print_warning "3. Configure your domain DNS settings"
print_warning "4. Set up SSL certificate"
print_warning "5. Create a superuser: python manage.py createsuperuser"

echo ""
print_status "🌐 Your website should be available at: https://$DOMAIN"
print_status "📊 Admin panel: https://$DOMAIN/admin/"
print_status "📧 Contact: contact@$DOMAIN"

# Deactivate virtual environment
deactivate
