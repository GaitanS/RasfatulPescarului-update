#!/bin/bash

# Backup script for Răsfățul Pescarului on Hostinger
# This script creates backups of database and media files

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PROJECT_NAME="RasfatulPescarului"
DOMAIN="rasfatul-pescarului.ro"
PROJECT_DIR="/home/u123456789/domains/$DOMAIN/public_html"
BACKUP_DIR="/home/u123456789/backups"
DATE=$(date +%Y%m%d_%H%M%S)

# Load environment variables
if [ -f "$PROJECT_DIR/.env" ]; then
    export $(cat "$PROJECT_DIR/.env" | grep -v '^#' | xargs)
fi

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

print_header() {
    echo -e "${BLUE}[BACKUP]${NC} $1"
}

# Create backup directory
print_status "Creating backup directory..."
mkdir -p "$BACKUP_DIR"

print_header "🗄️  Starting backup for Răsfățul Pescarului - $DATE"

# Database backup
if [ ! -z "$DB_NAME" ] && [ ! -z "$DB_USER" ] && [ ! -z "$DB_PASSWORD" ]; then
    print_status "Creating database backup..."
    
    DB_BACKUP_FILE="$BACKUP_DIR/database_${DATE}.sql"
    
    if mysqldump -h "$DB_HOST" -u "$DB_USER" -p"$DB_PASSWORD" "$DB_NAME" > "$DB_BACKUP_FILE"; then
        print_status "✅ Database backup created: $DB_BACKUP_FILE"
        
        # Compress database backup
        gzip "$DB_BACKUP_FILE"
        print_status "✅ Database backup compressed: ${DB_BACKUP_FILE}.gz"
    else
        print_error "❌ Failed to create database backup"
    fi
else
    print_warning "Database credentials not found in .env file"
fi

# Media files backup
print_status "Creating media files backup..."
MEDIA_BACKUP_FILE="$BACKUP_DIR/media_${DATE}.tar.gz"

if [ -d "$PROJECT_DIR/media" ]; then
    cd "$PROJECT_DIR"
    if tar -czf "$MEDIA_BACKUP_FILE" media/; then
        print_status "✅ Media files backup created: $MEDIA_BACKUP_FILE"
    else
        print_error "❌ Failed to create media files backup"
    fi
else
    print_warning "Media directory not found"
fi

# Static files backup (optional)
print_status "Creating static files backup..."
STATIC_BACKUP_FILE="$BACKUP_DIR/static_${DATE}.tar.gz"

if [ -d "$PROJECT_DIR/staticfiles" ]; then
    cd "$PROJECT_DIR"
    if tar -czf "$STATIC_BACKUP_FILE" staticfiles/; then
        print_status "✅ Static files backup created: $STATIC_BACKUP_FILE"
    else
        print_error "❌ Failed to create static files backup"
    fi
else
    print_warning "Static files directory not found"
fi

# Configuration backup
print_status "Creating configuration backup..."
CONFIG_BACKUP_FILE="$BACKUP_DIR/config_${DATE}.tar.gz"

cd "$PROJECT_DIR"
if tar -czf "$CONFIG_BACKUP_FILE" .env .htaccess passenger_wsgi.py requirements.txt; then
    print_status "✅ Configuration backup created: $CONFIG_BACKUP_FILE"
else
    print_error "❌ Failed to create configuration backup"
fi

# Full project backup (excluding large directories)
print_status "Creating full project backup..."
FULL_BACKUP_FILE="$BACKUP_DIR/full_project_${DATE}.tar.gz"

cd "$PROJECT_DIR"
if tar -czf "$FULL_BACKUP_FILE" \
    --exclude='staticfiles' \
    --exclude='media' \
    --exclude='__pycache__' \
    --exclude='.git' \
    --exclude='*.pyc' \
    --exclude='*.log' \
    .; then
    print_status "✅ Full project backup created: $FULL_BACKUP_FILE"
else
    print_error "❌ Failed to create full project backup"
fi

# Cleanup old backups (keep last 7 days)
print_status "Cleaning up old backups..."
find "$BACKUP_DIR" -name "*.sql.gz" -mtime +7 -delete 2>/dev/null || true
find "$BACKUP_DIR" -name "*.tar.gz" -mtime +7 -delete 2>/dev/null || true
print_status "✅ Old backups cleaned up"

# Display backup summary
print_header "📊 Backup Summary"
echo ""
echo "Backup location: $BACKUP_DIR"
echo "Backup date: $DATE"
echo ""
echo "Created files:"
ls -lh "$BACKUP_DIR"/*_${DATE}* 2>/dev/null || echo "No backup files found"
echo ""

# Calculate total backup size
TOTAL_SIZE=$(du -sh "$BACKUP_DIR" | cut -f1)
print_status "Total backup size: $TOTAL_SIZE"

# Create backup log
BACKUP_LOG="$BACKUP_DIR/backup.log"
echo "[$DATE] Backup completed successfully" >> "$BACKUP_LOG"

print_header "✅ Backup completed successfully!"
print_status "All backups are stored in: $BACKUP_DIR"
print_status "Log file: $BACKUP_LOG"

# Optional: Send backup notification email
if [ ! -z "$EMAIL_HOST_USER" ] && [ ! -z "$EMAIL_HOST_PASSWORD" ]; then
    print_status "Sending backup notification email..."
    
    # Create email content
    EMAIL_SUBJECT="Backup completed - Răsfățul Pescarului - $DATE"
    EMAIL_BODY="Backup for Răsfățul Pescarului has been completed successfully.

Date: $DATE
Total size: $TOTAL_SIZE
Location: $BACKUP_DIR

Files created:
$(ls -lh "$BACKUP_DIR"/*_${DATE}* 2>/dev/null || echo "No backup files found")

This is an automated message from the backup system."

    # Send email using Python (since we have Django available)
    cd "$PROJECT_DIR"
    source "/home/u123456789/virtualenv/$DOMAIN/bin/activate"
    
    python -c "
import os
import django
from django.conf import settings
from django.core.mail import send_mail

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'RasfatulPescarului.settings')
django.setup()

try:
    send_mail(
        '$EMAIL_SUBJECT',
        '''$EMAIL_BODY''',
        settings.EMAIL_HOST_USER,
        ['$EMAIL_HOST_USER'],
        fail_silently=False,
    )
    print('✅ Backup notification email sent')
except Exception as e:
    print(f'❌ Failed to send email: {e}')
" 2>/dev/null || print_warning "Failed to send backup notification email"
fi

echo ""
print_header "🎣 Răsfățul Pescarului backup completed! 🗄️"
