@echo off
REM Script pentru regenerarea cache-ului django-compressor pe Windows
REM Folosește acest script pentru a regenera fișierele comprimate local

echo.
echo ========================================
echo   Regenerare Cache Django-Compressor
echo ========================================
echo.

REM Verifică dacă mediul virtual există
if not exist "venv\Scripts\activate.bat" (
    echo ❌ Mediul virtual nu a fost găsit!
    echo 💡 Rulează mai întâi: python -m venv venv
    echo 💡 Apoi: venv\Scripts\activate
    echo 💡 Și: pip install -r requirements.txt
    pause
    exit /b 1
)

REM Activează mediul virtual
echo 🔄 Activez mediul virtual...
call venv\Scripts\activate.bat

REM Verifică dacă Django este instalat
python -c "import django" 2>nul
if errorlevel 1 (
    echo ❌ Django nu este instalat!
    echo 💡 Rulează: pip install -r requirements.txt
    pause
    exit /b 1
)

REM Șterge cache-ul existent
echo 🗑️  Șterg cache-ul existent...
if exist "staticfiles\CACHE" rmdir /s /q "staticfiles\CACHE"
if exist "static\CACHE" rmdir /s /q "static\CACHE"

REM Regenerează cache-ul compressor
echo 🔨 Generez cache-ul compressor...
python manage.py compress --force
if errorlevel 1 (
    echo ❌ Eroare la generarea cache-ului compressor!
    pause
    exit /b 1
)

REM Colectează fișierele statice
echo 📦 Colectez fișierele statice...
python manage.py collectstatic --noinput
if errorlevel 1 (
    echo ❌ Eroare la colectarea fișierelor statice!
    pause
    exit /b 1
)

REM Verifică rezultatul
echo.
echo 📊 Verificare rezultat...
if exist "staticfiles\CACHE\js" (
    echo ✅ Fișiere JS generate cu succes!
    dir /b "staticfiles\CACHE\js\*.js" 2>nul | find /c /v "" > temp_count.txt
    set /p js_count=<temp_count.txt
    del temp_count.txt
    echo    - Numărul de fișiere JS: %js_count%
) else (
    echo ⚠️  Nu s-au generat fișiere JS
)

if exist "staticfiles\CACHE\css" (
    echo ✅ Fișiere CSS generate cu succes!
    dir /b "staticfiles\CACHE\css\*.css" 2>nul | find /c /v "" > temp_count.txt
    set /p css_count=<temp_count.txt
    del temp_count.txt
    echo    - Numărul de fișiere CSS: %css_count%
) else (
    echo ⚠️  Nu s-au generat fișiere CSS
)

echo.
echo 🎉 Regenerarea cache-ului s-a finalizat cu succes!
echo 💡 Acum poți rula: python manage.py runserver
echo.
pause
