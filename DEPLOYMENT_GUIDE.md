# 🚀 Deployment Guide - Răsfățul Pescarului

## 🌐 Website Live
- **Production**: https://rasfatul-pescarului.ro
- **Admin Panel**: https://rasfatul-pescarului.ro/admin

## 💻 Dezvoltare Locală

### Prerequisite
- Python 3.11+
- Git

### Instalare
```bash
# Clonează repository-ul
git clone https://github.com/GaitanS/RasfatulPescarului-update.git
cd RasfatulPescarului-update

# Creează mediul virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# sau
venv\Scripts\activate  # Windows

# Instalează dependențele
pip install -r requirements.txt

# Configurează variabilele de mediu
# Pentru dezvoltare, .env este deja configurat pentru SQLite

# Rulează migrațiile
python manage.py migrate

# Creează superuser
python manage.py createsuperuser

# Colectează fișierele statice
python manage.py collectstatic

# Pornește serverul de dezvoltare
python manage.py runserver
```

## 🚀 Deployment pe Server

### Configurația Serverului
- **Server**: Ubuntu 25.04
- **IP**: 145.223.117.86
- **Domeniu**: rasfatul-pescarului.ro
- **Web Server**: Nginx + Gunicorn
- **Bază de Date**: PostgreSQL
- **SSL**: Let's Encrypt

### Deployment Automat
```bash
# Asigură-te că ai commit-at toate modificările
git add .
git commit -m "Descrierea modificărilor"

# Rulează scriptul de deployment
chmod +x deploy_to_server.sh
./deploy_to_server.sh
```

### Deployment Manual
```bash
# Conectează-te la server
ssh root@145.223.117.86

# Navighează la proiect
cd /var/www/RasfatulPescarului-update

# Pull modificările
git pull origin main

# Activează mediul virtual
source venv/bin/activate

# Instalează dependențele noi
pip install -r requirements.txt

# Rulează migrațiile
python manage.py migrate

# Colectează fișierele statice
python manage.py collectstatic --noinput

# Restartează serviciul
systemctl restart rasfatul-pescarului
```

## 🔧 Modificări Aplicate

### 1. Requirements.txt
- Actualizat cu dependențele necesare pentru producție
- Adăugat `python-dateutil` pentru solunar calendar
- Adăugat `whitenoise` pentru fișiere statice
- Adăugat `gunicorn` pentru server WSGI

### 2. Settings.py
- Schimbat ENGINE de la MySQL la PostgreSQL
- Dezactivat `COMPRESS_OFFLINE` pentru a evita erorile
- Configurat pentru a folosi SQLite în dezvoltare și PostgreSQL în producție

### 3. Configurare Mediu
- `.env` - configurație pentru dezvoltare locală (SQLite)
- `.env.production` - configurație pentru producție (PostgreSQL)

### 4. Script Deployment
- `deploy_to_server.sh` - script automat pentru deployment

## 📝 Comenzi Utile

```bash
# Dezvoltare
python manage.py runserver              # Pornește serverul local
python manage.py makemigrations         # Creează migrații
python manage.py migrate                # Aplică migrații
python manage.py createsuperuser        # Creează admin user
python manage.py collectstatic          # Colectează fișiere statice

# Django Compressor (pentru fișiere JS/CSS)
python manage.py compress --force       # Regenerează cache compressor
python regenerate_cache.py              # Script automat pentru cache
rm -rf staticfiles/CACHE/               # Șterge cache-ul manual

# Producție
systemctl status rasfatul-pescarului    # Status serviciu
systemctl restart rasfatul-pescarului   # Restart serviciu
tail -f /tmp/django.log                 # Vezi log-uri
nginx -t                                # Test configurație Nginx
```

## 🔐 Variabile de Mediu

### Dezvoltare (.env)
```env
DEBUG=True
SECRET_KEY=django-insecure-local-development-key
DB_NAME=                        # Gol pentru SQLite
```

### Producție (.env.production)
```env
DEBUG=False
SECRET_KEY=production-secret-key
DB_NAME=rasfatul_pescarului
DB_USER=rasfatul_user
DB_PASSWORD=MariusEnachi2025
DB_HOST=localhost
DB_PORT=5432
```

## 🐛 Troubleshooting

### Probleme Comune

1. **Eroare 500 - django-compressor**
   ```bash
   python manage.py compress --force
   python manage.py collectstatic --noinput
   ```

2. **JavaScript nu se încarcă (404 pe fișiere CACHE/js/) sau erori 500 intermitente**
   ```bash
   # SOLUȚIA RECOMANDATĂ: Dezactivează compressor complet
   # Editează settings.py și schimbă:
   # COMPRESS_ENABLED = not DEBUG
   # în:
   # COMPRESS_ENABLED = False

   # Apoi restartează serviciul
   systemctl restart rasfatul-pescarului

   # ALTERNATIV: Regenerează cache-ul (mai puțin stabil)
   rm -rf staticfiles/CACHE/
   python manage.py compress --force
   python manage.py collectstatic --noinput
   ```

3. **Probleme cu fișierele statice**
   - Verifică că WhiteNoise este în MIDDLEWARE
   - Rulează `collectstatic`
   - Verifică că `COMPRESS_OFFLINE = False` în settings.py

4. **Probleme cu baza de date**
   - Verifică configurația în .env
   - Testează conexiunea PostgreSQL

5. **Pagina de hartă nu funcționează**
   - Verifică că fișierele JS sunt generate în staticfiles/CACHE/js/
   - Verifică log-urile pentru erori 404 pe fișiere JS
   - Regenerează cache-ul compressor

## ✅ Status Deployment

- ✅ Requirements.txt actualizat
- ✅ Settings.py configurat pentru PostgreSQL
- ✅ COMPRESS_OFFLINE dezactivat
- ✅ Fișiere .env configurate
- ✅ Script deployment creat
- ✅ Website funcțional pe https://rasfatul-pescarului.ro
