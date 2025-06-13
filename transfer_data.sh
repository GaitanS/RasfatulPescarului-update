#!/bin/bash

# Script pentru transferul rapid al datelor din local pe server
# Exportă datele local, le transferă pe server și le importă

echo "🚀 Transfer rapid date: Local → Server"
echo "====================================="

# Verifică dacă mediul virtual local este activ
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "⚠️  Activează mediul virtual local mai întâi!"
    echo "💡 Rulează: source venv/bin/activate (Linux/Mac) sau venv\\Scripts\\activate (Windows)"
    exit 1
fi

# 1. Exportă datele din baza de date locală
echo "📤 1. Exportare date din baza de date locală..."
python export_data.py

if [ $? -ne 0 ]; then
    echo "❌ Exportul a eșuat!"
    exit 1
fi

if [ ! -f "database_export.json" ]; then
    echo "❌ Fișierul database_export.json nu a fost creat!"
    exit 1
fi

echo "✅ Export local complet!"

# 2. Transferă fișierul pe server
echo ""
echo "📡 2. Transfer fișier pe server..."
scp database_export.json import_data.py root@145.223.117.86:/var/www/RasfatulPescarului-update/

if [ $? -ne 0 ]; then
    echo "❌ Transferul pe server a eșuat!"
    exit 1
fi

echo "✅ Transfer complet!"

# 3. Importă datele pe server
echo ""
echo "📥 3. Import date pe server..."
ssh root@145.223.117.86 << 'EOF'
    cd /var/www/RasfatulPescarului-update
    source venv/bin/activate
    python import_data.py
EOF

if [ $? -ne 0 ]; then
    echo "❌ Importul pe server a eșuat!"
    exit 1
fi

# 4. Curățenie
echo ""
echo "🧹 4. Curățenie..."
rm -f database_export.json
ssh root@145.223.117.86 "rm -f /var/www/RasfatulPescarului-update/database_export.json"

echo ""
echo "🎉 Transfer complet finalizat!"
echo "✅ Toate datele au fost transferate cu succes pe server!"
echo ""
echo "🌐 Verifică pe: https://rasfatul-pescarului.ro/admin"
