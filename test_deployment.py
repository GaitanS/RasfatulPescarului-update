#!/usr/bin/env python3
"""
Deployment test script for Răsfățul Pescarului on Hostinger
This script tests various aspects of the deployment to ensure everything works correctly.
"""

import os
import sys
import requests
import subprocess
from urllib.parse import urljoin
import time

# Configuration
DOMAIN = "rasfatul-pescarului.ro"
BASE_URL = f"https://{DOMAIN}"
TIMEOUT = 30

# Test URLs
TEST_URLS = [
    "/",
    "/locations/",
    "/solunar-calendar/",
    "/admin/",
    "/static/css/style.css",
    "/static/js/script.js",
]

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_status(message, status="INFO"):
    color = Colors.BLUE
    if status == "SUCCESS":
        color = Colors.GREEN
    elif status == "ERROR":
        color = Colors.RED
    elif status == "WARNING":
        color = Colors.YELLOW
    
    print(f"{color}[{status}]{Colors.ENDC} {message}")

def test_url(url, expected_status=200):
    """Test if a URL is accessible and returns expected status code."""
    try:
        full_url = urljoin(BASE_URL, url)
        print_status(f"Testing {full_url}...")
        
        response = requests.get(full_url, timeout=TIMEOUT, allow_redirects=True)
        
        if response.status_code == expected_status:
            print_status(f"✅ {url} - OK (HTTP {response.status_code})", "SUCCESS")
            return True
        else:
            print_status(f"❌ {url} - Failed (HTTP {response.status_code})", "ERROR")
            return False
            
    except requests.exceptions.RequestException as e:
        print_status(f"❌ {url} - Connection error: {str(e)}", "ERROR")
        return False

def test_ssl_certificate():
    """Test SSL certificate validity."""
    try:
        print_status("Testing SSL certificate...")
        
        # Test HTTPS connection
        response = requests.get(BASE_URL, timeout=TIMEOUT)
        if response.url.startswith('https://'):
            print_status("✅ SSL certificate is working", "SUCCESS")
            return True
        else:
            print_status("❌ SSL redirect not working", "ERROR")
            return False
            
    except requests.exceptions.SSLError as e:
        print_status(f"❌ SSL certificate error: {str(e)}", "ERROR")
        return False
    except Exception as e:
        print_status(f"❌ SSL test failed: {str(e)}", "ERROR")
        return False

def test_database_connection():
    """Test database connection using Django management command."""
    try:
        print_status("Testing database connection...")
        
        # Change to project directory
        project_dir = "/home/u123456789/domains/rasfatul-pescarului.ro/public_html"
        if os.path.exists(project_dir):
            os.chdir(project_dir)
        
        # Activate virtual environment and test database
        venv_path = "/home/u123456789/virtualenv/rasfatul-pescarului.ro/bin/activate"
        if os.path.exists(venv_path):
            cmd = f"source {venv_path} && python manage.py check --database default"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                print_status("✅ Database connection is working", "SUCCESS")
                return True
            else:
                print_status(f"❌ Database connection failed: {result.stderr}", "ERROR")
                return False
        else:
            print_status("❌ Virtual environment not found", "ERROR")
            return False
            
    except Exception as e:
        print_status(f"❌ Database test failed: {str(e)}", "ERROR")
        return False

def test_static_files():
    """Test if static files are being served correctly."""
    try:
        print_status("Testing static files...")
        
        static_urls = [
            "/static/css/style.css",
            "/static/js/script.js",
            "/static/images/logo.png",
        ]
        
        success_count = 0
        for url in static_urls:
            if test_url(url):
                success_count += 1
        
        if success_count == len(static_urls):
            print_status("✅ All static files are accessible", "SUCCESS")
            return True
        else:
            print_status(f"⚠️  {success_count}/{len(static_urls)} static files accessible", "WARNING")
            return False
            
    except Exception as e:
        print_status(f"❌ Static files test failed: {str(e)}", "ERROR")
        return False

def test_admin_panel():
    """Test if admin panel is accessible."""
    try:
        print_status("Testing admin panel...")
        
        admin_url = urljoin(BASE_URL, "/admin/")
        response = requests.get(admin_url, timeout=TIMEOUT)
        
        # Admin should redirect to login or show login page
        if response.status_code in [200, 302] and ('login' in response.text.lower() or 'admin' in response.text.lower()):
            print_status("✅ Admin panel is accessible", "SUCCESS")
            return True
        else:
            print_status("❌ Admin panel not accessible", "ERROR")
            return False
            
    except Exception as e:
        print_status(f"❌ Admin panel test failed: {str(e)}", "ERROR")
        return False

def test_performance():
    """Test website performance (response time)."""
    try:
        print_status("Testing website performance...")
        
        start_time = time.time()
        response = requests.get(BASE_URL, timeout=TIMEOUT)
        end_time = time.time()
        
        response_time = end_time - start_time
        
        if response_time < 3.0:
            print_status(f"✅ Good response time: {response_time:.2f}s", "SUCCESS")
            return True
        elif response_time < 5.0:
            print_status(f"⚠️  Acceptable response time: {response_time:.2f}s", "WARNING")
            return True
        else:
            print_status(f"❌ Slow response time: {response_time:.2f}s", "ERROR")
            return False
            
    except Exception as e:
        print_status(f"❌ Performance test failed: {str(e)}", "ERROR")
        return False

def test_security_headers():
    """Test if security headers are present."""
    try:
        print_status("Testing security headers...")
        
        response = requests.get(BASE_URL, timeout=TIMEOUT)
        headers = response.headers
        
        security_headers = [
            'X-Frame-Options',
            'X-Content-Type-Options',
            'X-XSS-Protection',
        ]
        
        present_headers = []
        for header in security_headers:
            if header in headers:
                present_headers.append(header)
        
        if len(present_headers) >= 2:
            print_status(f"✅ Security headers present: {', '.join(present_headers)}", "SUCCESS")
            return True
        else:
            print_status(f"⚠️  Limited security headers: {', '.join(present_headers)}", "WARNING")
            return False
            
    except Exception as e:
        print_status(f"❌ Security headers test failed: {str(e)}", "ERROR")
        return False

def main():
    """Run all deployment tests."""
    print_status("🚀 Starting deployment tests for Răsfățul Pescarului", "INFO")
    print_status(f"Domain: {DOMAIN}", "INFO")
    print_status(f"Base URL: {BASE_URL}", "INFO")
    print("-" * 60)
    
    tests = [
        ("Website Accessibility", lambda: all(test_url(url) for url in TEST_URLS[:3])),
        ("SSL Certificate", test_ssl_certificate),
        ("Database Connection", test_database_connection),
        ("Static Files", test_static_files),
        ("Admin Panel", test_admin_panel),
        ("Performance", test_performance),
        ("Security Headers", test_security_headers),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print_status(f"\n🔍 Running {test_name} test...", "INFO")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print_status(f"❌ {test_name} test crashed: {str(e)}", "ERROR")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print_status("📊 DEPLOYMENT TEST SUMMARY", "INFO")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        color = Colors.GREEN if result else Colors.RED
        print(f"{color}{status}{Colors.ENDC} {test_name}")
        if result:
            passed += 1
    
    print("-" * 60)
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print_status("🎉 All tests passed! Deployment is successful!", "SUCCESS")
        return 0
    elif passed >= total * 0.8:
        print_status("⚠️  Most tests passed. Check failed tests.", "WARNING")
        return 1
    else:
        print_status("❌ Multiple tests failed. Deployment needs attention.", "ERROR")
        return 2

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print_status("\n🛑 Tests interrupted by user", "WARNING")
        sys.exit(130)
    except Exception as e:
        print_status(f"💥 Unexpected error: {str(e)}", "ERROR")
        sys.exit(1)
