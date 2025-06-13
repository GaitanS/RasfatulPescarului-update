#!/usr/bin/env python
"""
Script pentru verificarea configurației proiectului
Verifică dacă toate dependențele și configurațiile sunt corecte
"""

import os
import sys
import subprocess
from pathlib import Path

# Colors for terminal output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_status(message, status="info"):
    """Print colored status message"""
    if status == "success":
        print(f"{Colors.GREEN}✅ {message}{Colors.ENDC}")
    elif status == "error":
        print(f"{Colors.RED}❌ {message}{Colors.ENDC}")
    elif status == "warning":
        print(f"{Colors.YELLOW}⚠️  {message}{Colors.ENDC}")
    else:
        print(f"{Colors.BLUE}ℹ️  {message}{Colors.ENDC}")

def check_python_version():
    """Check Python version"""
    version = sys.version_info
    if version.major == 3 and version.minor >= 11:
        print_status(f"Python {version.major}.{version.minor}.{version.micro}", "success")
        return True
    else:
        print_status(f"Python {version.major}.{version.minor}.{version.micro} - Necesită Python 3.11+", "error")
        return False

def check_virtual_env():
    """Check if virtual environment is active"""
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print_status("Mediul virtual este activ", "success")
        return True
    else:
        print_status("Mediul virtual nu este activ", "warning")
        return False

def check_requirements():
    """Check if requirements are installed"""
    try:
        import django
        print_status(f"Django {django.get_version()}", "success")
    except ImportError:
        print_status("Django nu este instalat", "error")
        return False
    
    try:
        import compressor
        print_status("django-compressor instalat", "success")
    except ImportError:
        print_status("django-compressor nu este instalat", "error")
        return False
    
    return True

def check_env_file():
    """Check if .env file exists"""
    env_file = Path('.env')
    if env_file.exists():
        print_status(".env file există", "success")
        return True
    else:
        print_status(".env file nu există", "warning")
        print_status("Copiază .env.example la .env și configurează-l", "info")
        return False

def check_database():
    """Check database configuration"""
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'RasfatulPescarului.settings')
        import django
        django.setup()
        
        from django.core.management import execute_from_command_line
        from django.db import connection
        
        # Test database connection
        connection.ensure_connection()
        print_status("Conexiunea la baza de date funcționează", "success")
        return True
    except Exception as e:
        print_status(f"Problemă cu baza de date: {e}", "error")
        return False

def check_static_files():
    """Check static files configuration"""
    static_dir = Path('static')
    staticfiles_dir = Path('staticfiles')
    
    if static_dir.exists():
        print_status("Directorul static/ există", "success")
    else:
        print_status("Directorul static/ nu există", "error")
        return False
    
    # Check for important JS files
    js_files = ['script.js', 'adsense.js', 'solunar.js']
    missing_js = []
    
    for js_file in js_files:
        if not (static_dir / 'js' / js_file).exists():
            missing_js.append(js_file)
    
    if missing_js:
        print_status(f"Fișiere JS lipsă: {', '.join(missing_js)}", "warning")
    else:
        print_status("Toate fișierele JS principale există", "success")
    
    return True

def check_compressor_cache():
    """Check if compressor cache exists"""
    cache_dir = Path('staticfiles') / 'CACHE'
    
    if cache_dir.exists():
        js_files = list((cache_dir / 'js').glob('*.js')) if (cache_dir / 'js').exists() else []
        css_files = list((cache_dir / 'css').glob('*.css')) if (cache_dir / 'css').exists() else []
        
        if js_files or css_files:
            print_status(f"Cache compressor există ({len(js_files)} JS, {len(css_files)} CSS)", "success")
            return True
        else:
            print_status("Cache compressor gol", "warning")
            return False
    else:
        print_status("Cache compressor nu există", "warning")
        print_status("Rulează: python regenerate_cache.py", "info")
        return False

def main():
    """Main check function"""
    print(f"{Colors.BOLD}🔍 Verificare Configurație Răsfățul Pescarului{Colors.ENDC}")
    print("=" * 50)
    
    checks = [
        ("Versiune Python", check_python_version),
        ("Mediu Virtual", check_virtual_env),
        ("Dependențe", check_requirements),
        ("Fișier .env", check_env_file),
        ("Baza de Date", check_database),
        ("Fișiere Statice", check_static_files),
        ("Cache Compressor", check_compressor_cache),
    ]
    
    results = []
    
    for name, check_func in checks:
        print(f"\n📋 {name}:")
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print_status(f"Eroare la verificare: {e}", "error")
            results.append((name, False))
    
    # Summary
    print(f"\n{Colors.BOLD}📊 Rezumat:{Colors.ENDC}")
    print("=" * 30)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "success" if result else "error"
        print_status(f"{name}: {'OK' if result else 'FAIL'}", status)
    
    print(f"\n{Colors.BOLD}Rezultat: {passed}/{total} verificări trecute{Colors.ENDC}")
    
    if passed == total:
        print_status("🎉 Toate verificările au trecut! Proiectul este gata de rulare.", "success")
        print_status("💡 Rulează: python manage.py runserver", "info")
    else:
        print_status("⚠️  Unele verificări au eșuat. Vezi instrucțiunile de mai sus.", "warning")
        
        if not any(result for name, result in results if name == "Cache Compressor"):
            print_status("💡 Pentru a rezolva cache-ul: python regenerate_cache.py", "info")

if __name__ == '__main__':
    main()
