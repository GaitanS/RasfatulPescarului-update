# 🚀 Hostinger Deployment - Răsfățul Pescarului

## Quick Setup Guide

### 📋 Prerequisites
- Hostinger account with Python hosting
- Domain: `rasfatul-pescarului.ro`
- Server IP: `145.223.117.86`
- SSH access

### ⚡ Quick Deployment Commands

```bash
# 1. Connect to server
ssh u123456789@145.223.117.86

# 2. Navigate to domain directory
cd /home/u123456789/domains/rasfatul-pescarului.ro/public_html

# 3. Clone repository
git clone https://github.com/GaitanS/RasfatulPescarului-update.git .

# 4. Run deployment script
chmod +x deploy.sh
./deploy.sh

# 5. Configure environment
cp .env.example .env
nano .env  # Edit with your actual values

# 6. Setup database and static files
source /home/u123456789/virtualenv/rasfatul-pescarului.ro/bin/activate
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py compress --force
python manage.py createsuperuser
```

### 🔧 Essential Configuration

#### .env File (Required)
```env
DEBUG=False
SECRET_KEY=your-super-secret-key-here
SITE_URL=https://rasfatul-pescarului.ro

# Database (Create in Hostinger Control Panel)
DB_NAME=u123456789_rasfatul
DB_USER=u123456789_rasfatul
DB_PASSWORD=your_database_password
DB_HOST=localhost
DB_PORT=3306

# Email (Setup in Hostinger)
EMAIL_HOST=smtp.hostinger.com
EMAIL_PORT=587
EMAIL_HOST_USER=contact@rasfatul-pescarului.ro
EMAIL_HOST_PASSWORD=your_email_password
```

#### Hostinger Control Panel Setup
1. **Database**: Create MySQL database
2. **Email**: Setup email account
3. **SSL**: Enable Let's Encrypt
4. **DNS**: Point domain to server IP

### 📁 File Structure
```
/home/u123456789/domains/rasfatul-pescarului.ro/public_html/
├── .env                    # Environment variables
├── .htaccess              # Apache configuration
├── passenger_wsgi.py      # WSGI entry point
├── manage.py              # Django management
├── requirements.txt       # Python dependencies
├── deploy.sh             # Deployment script
├── backup.sh             # Backup script
├── monitor.sh            # Monitoring script
├── static/               # Static files
├── media/                # User uploads
├── templates/            # HTML templates
└── RasfatulPescarului/   # Django project
```

### 🔄 Maintenance Commands

#### Update Website
```bash
cd /home/u123456789/domains/rasfatul-pescarului.ro/public_html
git pull origin main
source /home/u123456789/virtualenv/rasfatul-pescarului.ro/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py compress --force
```

#### Backup
```bash
./backup.sh
```

#### Monitor
```bash
./monitor.sh
```

### 🔍 Troubleshooting

#### Common Issues

**500 Error**
```bash
tail -f /tmp/django.log
tail -f /tmp/django_error.log
```

**Static Files Not Loading**
```bash
python manage.py collectstatic --clear --noinput
```

**Database Connection Error**
- Check .env file credentials
- Verify database exists in Hostinger panel

**Email Not Working**
- Verify email account in Hostinger
- Check SMTP settings in .env

### 📊 Monitoring Setup

#### Cron Jobs (Optional)
```bash
crontab -e
# Add these lines:
0 2 * * * /home/u123456789/domains/rasfatul-pescarului.ro/public_html/backup.sh
0 * * * * /home/u123456789/domains/rasfatul-pescarului.ro/public_html/monitor.sh
```

### 🌐 URLs to Test

After deployment, verify these URLs work:
- https://rasfatul-pescarului.ro
- https://rasfatul-pescarului.ro/admin/
- https://rasfatul-pescarului.ro/locations/
- https://rasfatul-pescarului.ro/solunar-calendar/

### 📞 Support

- **Repository**: https://github.com/GaitanS/RasfatulPescarului-update
- **Hostinger Support**: support@hostinger.com
- **Email**: contact@rasfatul-pescarului.ro

### ✅ Deployment Checklist

- [ ] Server access confirmed
- [ ] Repository cloned
- [ ] Virtual environment created
- [ ] Dependencies installed
- [ ] Database created and configured
- [ ] .env file configured
- [ ] Static files collected
- [ ] Database migrated
- [ ] Superuser created
- [ ] SSL certificate enabled
- [ ] Domain DNS configured
- [ ] Website accessible
- [ ] Admin panel working
- [ ] Email functionality tested
- [ ] Backup script tested
- [ ] Monitoring setup

🎣 **Ready to go live!** 🌐
