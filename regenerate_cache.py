#!/usr/bin/env python
"""
Script pentru regenerarea cache-ului django-compressor
Folosește acest script pentru a regenera fișierele comprimate local
"""

import os
import sys
import django
from pathlib import Path

# Add the project directory to the Python path
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'RasfatulPescarului.settings')
django.setup()

from django.core.management import call_command
from django.conf import settings
import shutil

def regenerate_cache():
    """Regenerează cache-ul django-compressor"""
    print("🔄 Regenerare cache django-compressor...")
    
    # Șterge cache-ul existent
    cache_dirs = [
        BASE_DIR / 'staticfiles' / 'CACHE',
        BASE_DIR / 'static' / 'CACHE',
    ]
    
    for cache_dir in cache_dirs:
        if cache_dir.exists():
            print(f"🗑️  Șterg cache-ul din {cache_dir}")
            shutil.rmtree(cache_dir)
    
    # Regenerează cache-ul
    try:
        print("🔨 Generez cache-ul compressor...")
        call_command('compress', '--force', verbosity=2)
        print("✅ Cache-ul compressor a fost generat cu succes!")
    except Exception as e:
        print(f"❌ Eroare la generarea cache-ului: {e}")
        return False
    
    # Colectează fișierele statice
    try:
        print("📦 Colectez fișierele statice...")
        call_command('collectstatic', '--noinput', verbosity=1)
        print("✅ Fișierele statice au fost colectate cu succes!")
    except Exception as e:
        print(f"❌ Eroare la colectarea fișierelor statice: {e}")
        return False
    
    return True

def check_cache():
    """Verifică dacă cache-ul a fost generat corect"""
    cache_dir = BASE_DIR / 'staticfiles' / 'CACHE'
    
    if not cache_dir.exists():
        print("❌ Directorul CACHE nu există")
        return False
    
    js_dir = cache_dir / 'js'
    css_dir = cache_dir / 'css'
    
    js_files = list(js_dir.glob('*.js')) if js_dir.exists() else []
    css_files = list(css_dir.glob('*.css')) if css_dir.exists() else []
    
    print(f"📊 Statistici cache:")
    print(f"   - Fișiere JS: {len(js_files)}")
    print(f"   - Fișiere CSS: {len(css_files)}")
    
    if js_files:
        print("📄 Fișiere JS generate:")
        for js_file in js_files:
            print(f"   - {js_file.name}")
    
    if css_files:
        print("📄 Fișiere CSS generate:")
        for css_file in css_files:
            print(f"   - {css_file.name}")
    
    return len(js_files) > 0 or len(css_files) > 0

if __name__ == '__main__':
    print("🚀 Începe regenerarea cache-ului django-compressor...")
    print(f"📁 Director proiect: {BASE_DIR}")
    print(f"⚙️  DEBUG: {settings.DEBUG}")
    print(f"🔧 COMPRESS_ENABLED: {settings.COMPRESS_ENABLED}")
    print(f"📴 COMPRESS_OFFLINE: {settings.COMPRESS_OFFLINE}")
    print()
    
    if regenerate_cache():
        print()
        check_cache()
        print()
        print("🎉 Regenerarea cache-ului s-a finalizat cu succes!")
        print("💡 Acum poți rula: python manage.py runserver")
    else:
        print()
        print("❌ Regenerarea cache-ului a eșuat!")
        sys.exit(1)
