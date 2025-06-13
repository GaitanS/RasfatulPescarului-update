#!/bin/bash

# Script pentru deployment pe server
# Folosește acest script pentru a sincroniza modificările cu serverul

echo "=== Deployment Script pentru Răsfățul Pescarului ==="

# Verifică dacă există modificări uncommitted
if [[ -n $(git status --porcelain) ]]; then
    echo "⚠️  Există modificări uncommitted. Commit-ează mai întâi modificările."
    git status
    exit 1
fi

# Push modificările pe GitHub
echo "📤 Push modificări pe GitHub..."
git push origin main

# Conectează-te la server și actualizează
echo "🚀 Conectare la server și actualizare..."
ssh root@145.223.117.86 << 'EOF'
    cd /var/www/RasfatulPescarului-update
    
    # Pull ultimele modificări
    git pull origin main
    
    # Activează mediul virtual
    source venv/bin/activate
    
    # Instalează dependențele noi
    pip install -r requirements.txt
    
    # Rulează migrațiile
    python manage.py migrate
    
    # Colectează fișierele statice
    python manage.py collectstatic --noinput

    # Creează imagini placeholder dacă lipsesc
    python create_placeholder_image.py

    # Corectează slug-urile județelor dacă e necesar
    python fix_county_slugs.py 2>/dev/null || echo "⚠️  Fix county slugs skipped (model might not have slug field)"

    # Restartează serviciul
    systemctl restart rasfatul-pescarului
    
    # Verifică statusul
    systemctl status rasfatul-pescarului --no-pager
    
    echo "✅ Deployment complet!"
EOF

echo "🎉 Deployment finalizat cu succes!"
echo "🌐 Website: https://rasfatul-pescarului.ro"
