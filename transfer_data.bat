@echo off
REM Script pentru transferul rapid al datelor din local pe server (Windows)
REM Exportă datele local, le transferă pe server și le importă

echo.
echo ========================================
echo   Transfer rapid date: Local -^> Server
echo ========================================
echo.

REM Verifică dacă mediul virtual există
if not exist "venv\Scripts\activate.bat" (
    echo ❌ Mediul virtual nu a fost găsit!
    echo 💡 Rulează mai întâi: python -m venv venv
    echo 💡 Apoi: venv\Scripts\activate
    pause
    exit /b 1
)

REM Activează mediul virtual
echo 🔄 Activez mediul virtual...
call venv\Scripts\activate.bat

REM 1. Exportă datele din baza de date locală
echo.
echo 📤 1. Exportare date din baza de date locală...
python export_data.py

if errorlevel 1 (
    echo ❌ Exportul a eșuat!
    pause
    exit /b 1
)

if not exist "database_export.json" (
    echo ❌ Fișierul database_export.json nu a fost creat!
    pause
    exit /b 1
)

echo ✅ Export local complet!

REM 2. Transferă fișierul pe server (necesită scp sau pscp)
echo.
echo 📡 2. Transfer fișier pe server...
echo 💡 Transferând database_export.json și import_data.py...

REM Încearcă cu scp (dacă este disponibil)
scp database_export.json import_data.py root@145.223.117.86:/var/www/RasfatulPescarului-update/ 2>nul

if errorlevel 1 (
    echo ⚠️  scp nu este disponibil. Încearcă cu pscp...
    pscp database_export.json import_data.py root@145.223.117.86:/var/www/RasfatulPescarului-update/
    
    if errorlevel 1 (
        echo ❌ Transferul a eșuat!
        echo 💡 Instalează OpenSSH sau PuTTY pentru transfer
        echo 💡 Sau copiază manual fișierele:
        echo    - database_export.json
        echo    - import_data.py
        echo 💡 Pe server în: /var/www/RasfatulPescarului-update/
        pause
        exit /b 1
    )
)

echo ✅ Transfer complet!

REM 3. Importă datele pe server
echo.
echo 📥 3. Import date pe server...
echo 💡 Conectare la server pentru import...

ssh root@145.223.117.86 "cd /var/www/RasfatulPescarului-update && source venv/bin/activate && python import_data.py"

if errorlevel 1 (
    echo ❌ Importul pe server a eșuat!
    echo 💡 Conectează-te manual la server și rulează:
    echo    cd /var/www/RasfatulPescarului-update
    echo    source venv/bin/activate
    echo    python import_data.py
    pause
    exit /b 1
)

REM 4. Curățenie
echo.
echo 🧹 4. Curățenie...
if exist "database_export.json" del "database_export.json"
ssh root@145.223.117.86 "rm -f /var/www/RasfatulPescarului-update/database_export.json" 2>nul

echo.
echo 🎉 Transfer complet finalizat!
echo ✅ Toate datele au fost transferate cu succes pe server!
echo.
echo 🌐 Verifică pe: https://rasfatul-pescarului.ro/admin
echo.
pause
