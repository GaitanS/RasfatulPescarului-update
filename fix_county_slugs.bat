@echo off
REM Script pentru corectarea slug-urilor județelor pe Windows

echo.
echo ========================================
echo   Fix County Slugs - Răsfățul Pescarului
echo ========================================
echo.

REM Verifică dacă mediul virtual există
if not exist "venv\Scripts\activate.bat" (
    echo ❌ Mediul virtual nu a fost găsit!
    echo 💡 Rulează mai întâi: python -m venv venv
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

REM Rulează scriptul de corectare
echo 🔧 Corectez slug-urile județelor...
python fix_county_slugs.py
if errorlevel 1 (
    echo ❌ Eroare la corectarea slug-urilor!
    pause
    exit /b 1
)

echo.
echo 🎉 Slug-urile au fost corectate cu succes!
echo 💡 Acum poți rula: python manage.py runserver
echo.
pause
