# Deployment Guide - Răsfățul Pescarului pe Hostinger

## 📋 Cerințe preliminare

### Hostinger Account Setup
- Cont Hostinger cu hosting Python/Django
- Domeniu: `rasfatul-pescarului.ro`
- Server IP: `145.223.117.86`
- Acces SSH la server

### Servicii necesare
- MySQL Database (prin Hostinger control panel)
- Email hosting (contact@rasfatul-pescarului.ro)
- SSL Certificate (Let's Encrypt prin Hostinger)

## 🚀 Pași de deployment

### 1. Pregătirea serverului

```bash
# Conectare SSH la server
ssh u123456789@145.223.117.86

# Actualizare sistem (dacă aveți permisiuni)
# sudo apt update && sudo apt upgrade -y

# Verificare versiune Python
python3 --version
```

### 2. Clonarea repository-ului

```bash
# Navigare la directorul domeniului
cd /home/u123456789/domains/rasfatul-pescarului.ro/public_html

# Clonare repository
git clone https://github.com/GaitanS/RasfatulPescarului-update.git .

# Sau dacă directorul nu este gol
git clone https://github.com/GaitanS/RasfatulPescarului-update.git temp
mv temp/* .
mv temp/.* . 2>/dev/null || true
rmdir temp
```

### 3. Configurarea mediului virtual

```bash
# Creare virtual environment
python3 -m venv /home/u123456789/virtualenv/rasfatul-pescarului.ro

# Activare virtual environment
source /home/u123456789/virtualenv/rasfatul-pescarului.ro/bin/activate

# Upgrade pip
pip install --upgrade pip

# Instalare dependințe
pip install -r requirements.txt
```

### 4. Configurarea bazei de date

#### În Hostinger Control Panel:
1. Accesați secțiunea "Databases"
2. Creați o nouă bază de date MySQL:
   - Database name: `u123456789_rasfatul`
   - Username: `u123456789_rasfatul`
   - Password: `[generat automat]`

#### Configurare .env:
```bash
# Copiere fișier de configurare
cp .env.example .env

# Editare configurații
nano .env
```

Conținut .env:
```env
DEBUG=False
SECRET_KEY=your-super-secret-key-here-generate-new-one
SITE_URL=https://rasfatul-pescarului.ro

# Database
DB_NAME=u123456789_rasfatul
DB_USER=u123456789_rasfatul
DB_PASSWORD=your_database_password
DB_HOST=localhost
DB_PORT=3306

# Email
EMAIL_HOST=smtp.hostinger.com
EMAIL_PORT=587
EMAIL_HOST_USER=contact@rasfatul-pescarului.ro
EMAIL_HOST_PASSWORD=your_email_password
```

### 5. Configurarea Django

```bash
# Activare virtual environment
source /home/u123456789/virtualenv/rasfatul-pescarului.ro/bin/activate

# Migrări bază de date
python manage.py migrate

# Colectare fișiere statice
python manage.py collectstatic --noinput

# Compresare fișiere statice
python manage.py compress --force

# Creare superuser
python manage.py createsuperuser
```

### 6. Configurarea permisiunilor

```bash
# Setare permisiuni fișiere
find . -type f -exec chmod 644 {} \;
find . -type d -exec chmod 755 {} \;
chmod +x manage.py

# Creare directoare necesare
mkdir -p media/uploads
mkdir -p logs
```

### 7. Configurarea domeniului

#### DNS Settings (în Hostinger):
- A Record: `@` → `145.223.117.86`
- A Record: `www` → `145.223.117.86`
- CNAME Record: `www` → `rasfatul-pescarului.ro`

#### SSL Certificate:
1. În Hostinger Control Panel → SSL
2. Activați Let's Encrypt pentru domeniu
3. Forțați HTTPS redirect

## 🔧 Configurări specifice Hostinger

### passenger_wsgi.py
Fișierul este deja configurat pentru Hostinger. Acesta:
- Încarcă variabilele de mediu din .env
- Configurează calea Python
- Gestionează erorile Django

### .htaccess
Configurează:
- HTTPS redirect
- Security headers
- Compresie fișiere
- Cache control
- Protecție fișiere sensibile

## 📊 Verificări post-deployment

### 1. Testare funcționalitate
```bash
# Test conexiune bază de date
python manage.py dbshell

# Test email
python manage.py shell
>>> from django.core.mail import send_mail
>>> send_mail('Test', 'Test message', 'contact@rasfatul-pescarului.ro', ['admin@rasfatul-pescarului.ro'])
```

### 2. Verificare URL-uri
- https://rasfatul-pescarului.ro - Homepage
- https://rasfatul-pescarului.ro/admin/ - Admin panel
- https://rasfatul-pescarului.ro/locations/ - Locations page
- https://rasfatul-pescarului.ro/solunar-calendar/ - Solunar calendar

### 3. Testare mobile
- Verificare responsive design
- Testare funcționalitate touch
- Verificare viteza încărcare

## 🔄 Actualizări viitoare

### Script de update
```bash
#!/bin/bash
cd /home/u123456789/domains/rasfatul-pescarului.ro/public_html
source /home/u123456789/virtualenv/rasfatul-pescarului.ro/bin/activate

git pull origin main
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py compress --force

echo "Update completed!"
```

### Backup bază de date
```bash
# Backup
mysqldump -u u123456789_rasfatul -p u123456789_rasfatul > backup_$(date +%Y%m%d).sql

# Restore
mysql -u u123456789_rasfatul -p u123456789_rasfatul < backup_20250613.sql
```

## 🐛 Troubleshooting

### Probleme comune

#### 1. Eroare 500 - Internal Server Error
```bash
# Verificare log-uri
tail -f /tmp/django.log
tail -f /tmp/django_error.log
```

#### 2. Static files nu se încarcă
```bash
# Re-colectare static files
python manage.py collectstatic --clear --noinput
```

#### 3. Database connection error
- Verificați credențialele în .env
- Testați conexiunea MySQL manual

#### 4. Email nu funcționează
- Verificați setările SMTP în .env
- Testați cu un client email extern

### Log files importante
- `/tmp/django.log` - Django application logs
- `/tmp/django_error.log` - Django error logs
- Hostinger control panel → Error Logs

## 📞 Support

### Contacte
- **Dezvoltator**: [GitHub Issues](https://github.com/GaitanS/RasfatulPescarului-update/issues)
- **Hostinger Support**: support@hostinger.com
- **Email tehnic**: contact@rasfatul-pescarului.ro

### Resurse utile
- [Hostinger Python Hosting Guide](https://support.hostinger.com/en/articles/1583579-how-to-set-up-python-on-shared-hosting)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/)
- [WhiteNoise Documentation](http://whitenoise.evans.io/)

## ✅ Checklist final

- [ ] Repository clonat și configurat
- [ ] Virtual environment creat și activat
- [ ] Dependințe instalate
- [ ] Baza de date configurată și migrată
- [ ] Fișier .env configurat cu valorile corecte
- [ ] Static files colectate și comprimate
- [ ] Superuser creat
- [ ] Permisiuni fișiere setate
- [ ] DNS configurat
- [ ] SSL activat
- [ ] Website accesibil la https://rasfatul-pescarului.ro
- [ ] Admin panel funcțional
- [ ] Email funcțional
- [ ] AdSense configurat și funcțional
- [ ] Mobile responsive verificat

🎣 **Răsfățul Pescarului este acum live pe Hostinger!** 🌐
