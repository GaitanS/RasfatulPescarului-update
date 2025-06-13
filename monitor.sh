#!/bin/bash

# Monitoring script for Răsfățul Pescarului on Hostinger
# This script checks website health and sends alerts if needed

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
DOMAIN="rasfatul-pescarului.ro"
PROJECT_DIR="/home/u123456789/domains/$DOMAIN/public_html"
LOG_DIR="/home/u123456789/backups"
HEALTH_LOG="$LOG_DIR/health_check.log"
DATE=$(date '+%Y-%m-%d %H:%M:%S')

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
    echo -e "${BLUE}[MONITOR]${NC} $1"
}

# Function to log messages
log_message() {
    echo "[$DATE] $1" >> "$HEALTH_LOG"
}

# Function to send alert email
send_alert() {
    local subject="$1"
    local message="$2"
    
    if [ ! -z "$EMAIL_HOST_USER" ] && [ ! -z "$EMAIL_HOST_PASSWORD" ]; then
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
        '$subject',
        '''$message''',
        settings.EMAIL_HOST_USER,
        ['$EMAIL_HOST_USER'],
        fail_silently=False,
    )
    print('Alert email sent')
except Exception as e:
    print(f'Failed to send alert email: {e}')
" 2>/dev/null
    fi
}

print_header "🔍 Starting health check for Răsfățul Pescarului"

# Create log directory if it doesn't exist
mkdir -p "$LOG_DIR"

# 1. Check website availability
print_status "Checking website availability..."
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "https://$DOMAIN" || echo "000")

if [ "$HTTP_CODE" = "200" ]; then
    print_status "✅ Website is accessible (HTTP $HTTP_CODE)"
    log_message "Website check: OK (HTTP $HTTP_CODE)"
else
    print_error "❌ Website is not accessible (HTTP $HTTP_CODE)"
    log_message "Website check: FAILED (HTTP $HTTP_CODE)"
    send_alert "Website Down - Răsfățul Pescarului" "Website https://$DOMAIN is not accessible. HTTP code: $HTTP_CODE"
fi

# 2. Check SSL certificate
print_status "Checking SSL certificate..."
SSL_EXPIRY=$(echo | openssl s_client -servername "$DOMAIN" -connect "$DOMAIN:443" 2>/dev/null | openssl x509 -noout -dates | grep notAfter | cut -d= -f2)

if [ ! -z "$SSL_EXPIRY" ]; then
    SSL_EXPIRY_EPOCH=$(date -d "$SSL_EXPIRY" +%s)
    CURRENT_EPOCH=$(date +%s)
    DAYS_UNTIL_EXPIRY=$(( (SSL_EXPIRY_EPOCH - CURRENT_EPOCH) / 86400 ))
    
    if [ $DAYS_UNTIL_EXPIRY -gt 30 ]; then
        print_status "✅ SSL certificate is valid ($DAYS_UNTIL_EXPIRY days remaining)"
        log_message "SSL check: OK ($DAYS_UNTIL_EXPIRY days remaining)"
    elif [ $DAYS_UNTIL_EXPIRY -gt 7 ]; then
        print_warning "⚠️  SSL certificate expires soon ($DAYS_UNTIL_EXPIRY days remaining)"
        log_message "SSL check: WARNING ($DAYS_UNTIL_EXPIRY days remaining)"
        send_alert "SSL Certificate Expiring Soon - Răsfățul Pescarului" "SSL certificate for $DOMAIN expires in $DAYS_UNTIL_EXPIRY days."
    else
        print_error "❌ SSL certificate expires very soon ($DAYS_UNTIL_EXPIRY days remaining)"
        log_message "SSL check: CRITICAL ($DAYS_UNTIL_EXPIRY days remaining)"
        send_alert "SSL Certificate Expiring - Răsfățul Pescarului" "SSL certificate for $DOMAIN expires in $DAYS_UNTIL_EXPIRY days. Immediate action required!"
    fi
else
    print_error "❌ Could not check SSL certificate"
    log_message "SSL check: FAILED (could not retrieve certificate)"
fi

# 3. Check database connectivity
print_status "Checking database connectivity..."
if [ ! -z "$DB_NAME" ] && [ ! -z "$DB_USER" ] && [ ! -z "$DB_PASSWORD" ]; then
    if mysql -h "$DB_HOST" -u "$DB_USER" -p"$DB_PASSWORD" -e "SELECT 1;" "$DB_NAME" >/dev/null 2>&1; then
        print_status "✅ Database connection is working"
        log_message "Database check: OK"
    else
        print_error "❌ Database connection failed"
        log_message "Database check: FAILED"
        send_alert "Database Connection Failed - Răsfățul Pescarului" "Cannot connect to MySQL database for $DOMAIN."
    fi
else
    print_warning "Database credentials not found in .env file"
fi

# 4. Check disk space
print_status "Checking disk space..."
DISK_USAGE=$(df -h /home/u123456789 | awk 'NR==2 {print $5}' | sed 's/%//')

if [ $DISK_USAGE -lt 80 ]; then
    print_status "✅ Disk space is OK (${DISK_USAGE}% used)"
    log_message "Disk space check: OK (${DISK_USAGE}% used)"
elif [ $DISK_USAGE -lt 90 ]; then
    print_warning "⚠️  Disk space is getting low (${DISK_USAGE}% used)"
    log_message "Disk space check: WARNING (${DISK_USAGE}% used)"
    send_alert "Low Disk Space - Răsfățul Pescarului" "Disk space is at ${DISK_USAGE}% on server for $DOMAIN."
else
    print_error "❌ Disk space is critically low (${DISK_USAGE}% used)"
    log_message "Disk space check: CRITICAL (${DISK_USAGE}% used)"
    send_alert "Critical Disk Space - Răsfățul Pescarului" "Disk space is critically low at ${DISK_USAGE}% on server for $DOMAIN. Immediate action required!"
fi

# 5. Check important pages
print_status "Checking important pages..."
PAGES=("/" "/admin/" "/locations/" "/solunar-calendar/")

for page in "${PAGES[@]}"; do
    PAGE_CODE=$(curl -s -o /dev/null -w "%{http_code}" "https://$DOMAIN$page" || echo "000")
    
    if [ "$PAGE_CODE" = "200" ] || [ "$PAGE_CODE" = "302" ]; then
        print_status "✅ Page $page is accessible (HTTP $PAGE_CODE)"
        log_message "Page check $page: OK (HTTP $PAGE_CODE)"
    else
        print_error "❌ Page $page is not accessible (HTTP $PAGE_CODE)"
        log_message "Page check $page: FAILED (HTTP $PAGE_CODE)"
        send_alert "Page Not Accessible - Răsfățul Pescarului" "Page https://$DOMAIN$page is not accessible. HTTP code: $PAGE_CODE"
    fi
done

# 6. Check log file sizes
print_status "Checking log file sizes..."
if [ -f "/tmp/django.log" ]; then
    LOG_SIZE=$(du -m "/tmp/django.log" | cut -f1)
    if [ $LOG_SIZE -gt 100 ]; then
        print_warning "⚠️  Django log file is large (${LOG_SIZE}MB)"
        log_message "Log size check: WARNING (${LOG_SIZE}MB)"
    else
        print_status "✅ Django log file size is OK (${LOG_SIZE}MB)"
        log_message "Log size check: OK (${LOG_SIZE}MB)"
    fi
fi

# 7. Check Python processes
print_status "Checking Python processes..."
PYTHON_PROCESSES=$(ps aux | grep python | grep -v grep | wc -l)
print_status "Python processes running: $PYTHON_PROCESSES"
log_message "Python processes: $PYTHON_PROCESSES"

# 8. Generate summary report
print_header "📊 Health Check Summary"
echo ""
echo "Domain: $DOMAIN"
echo "Check time: $DATE"
echo "Website status: HTTP $HTTP_CODE"
echo "SSL days remaining: $DAYS_UNTIL_EXPIRY"
echo "Disk usage: ${DISK_USAGE}%"
echo "Python processes: $PYTHON_PROCESSES"
echo ""

# Clean up old health check logs (keep last 30 days)
find "$LOG_DIR" -name "health_check.log.*" -mtime +30 -delete 2>/dev/null || true

print_header "✅ Health check completed!"
print_status "Log file: $HEALTH_LOG"

echo ""
print_header "🎣 Răsfățul Pescarului monitoring completed! 📊"
