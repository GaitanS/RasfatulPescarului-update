#!/usr/bin/env python3
"""
WSGI configuration for Răsfățul Pescarului on Hostinger.

This module contains the WSGI application used by Hostinger's Python hosting.
It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os
import sys
from pathlib import Path

# Add the project directory to the Python path
project_dir = Path(__file__).parent
sys.path.insert(0, str(project_dir))

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'RasfatulPescarului.settings')

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    env_path = project_dir / '.env'
    if env_path.exists():
        load_dotenv(env_path)
except ImportError:
    # python-dotenv not installed, skip loading .env file
    pass

# Import Django WSGI application
try:
    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()
except Exception as e:
    # Log the error for debugging
    import traceback
    error_msg = f"Error loading Django application: {str(e)}\n{traceback.format_exc()}"
    
    # Write error to a log file
    try:
        with open('/tmp/django_error.log', 'w') as f:
            f.write(error_msg)
    except:
        pass
    
    # Create a simple WSGI application that shows the error
    def application(environ, start_response):
        status = '500 Internal Server Error'
        headers = [('Content-type', 'text/html; charset=utf-8')]
        start_response(status, headers)
        
        error_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Server Error - Răsfățul Pescarului</title>
            <meta charset="utf-8">
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }}
                .container {{ max-width: 800px; margin: 0 auto; background: white; padding: 40px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
                h1 {{ color: #d32f2f; }}
                .error {{ background: #ffebee; padding: 20px; border-radius: 4px; margin: 20px 0; }}
                .code {{ background: #f5f5f5; padding: 10px; border-radius: 4px; font-family: monospace; white-space: pre-wrap; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🐟 Răsfățul Pescarului - Server Error</h1>
                <div class="error">
                    <p><strong>Ne pare rău, dar a apărut o eroare pe server.</strong></p>
                    <p>Echipa noastră a fost notificată și lucrează la rezolvarea problemei.</p>
                </div>
                <details>
                    <summary>Detalii tehnice (pentru dezvoltatori)</summary>
                    <div class="code">{error_msg}</div>
                </details>
                <p><a href="/">← Înapoi la pagina principală</a></p>
            </div>
        </body>
        </html>
        """.encode('utf-8')
        
        return [error_html]

# For debugging purposes, you can uncomment the following lines
# to see what's in the environment
"""
def debug_application(environ, start_response):
    status = '200 OK'
    headers = [('Content-type', 'text/html; charset=utf-8')]
    start_response(status, headers)
    
    debug_info = f'''
    <!DOCTYPE html>
    <html>
    <head><title>Debug Info</title></head>
    <body>
        <h1>Debug Information</h1>
        <h2>Python Path:</h2>
        <pre>{chr(10).join(sys.path)}</pre>
        
        <h2>Environment Variables:</h2>
        <pre>{chr(10).join(f"{k}={v}" for k, v in sorted(os.environ.items()))}</pre>
        
        <h2>Project Directory:</h2>
        <pre>{project_dir}</pre>
        
        <h2>Files in Project Directory:</h2>
        <pre>{chr(10).join(str(p) for p in project_dir.iterdir())}</pre>
    </body>
    </html>
    '''.encode('utf-8')
    
    return [debug_info]

# Uncomment the next line to use debug application instead
# application = debug_application
"""
