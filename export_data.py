#!/usr/bin/env python
"""
Script pentru exportul datelor din baza de date locală
Exportă județe, facilități și specii de pești în format JSON
"""

import os
import sys
import django
import json
from pathlib import Path

# Setup Django
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'RasfatulPescarului.settings')
django.setup()

from main.models import County, Facility, FishSpecies

def export_counties():
    """Exportă toate județele"""
    counties = []
    for county in County.objects.all().order_by('name'):
        counties.append({
            'name': county.name,
            'slug': county.slug,
            'latitude': float(county.latitude) if county.latitude else None,
            'longitude': float(county.longitude) if county.longitude else None,
            'description': county.description or '',
        })
    return counties

def export_facilities():
    """Exportă toate facilitățile"""
    facilities = []
    for facility in Facility.objects.all().order_by('name'):
        facilities.append({
            'name': facility.name,
            'icon': facility.icon,
            'description': facility.description or '',
        })
    return facilities

def export_fish_species():
    """Exportă toate speciile de pești"""
    fish_species = []
    for fish in FishSpecies.objects.all().order_by('name'):
        fish_species.append({
            'name': fish.name,
            'scientific_name': fish.scientific_name or '',
            'description': fish.description or '',
            'min_weight': float(fish.min_weight) if fish.min_weight else None,
            'max_weight': float(fish.max_weight) if fish.max_weight else None,
            'season_start': fish.season_start.strftime('%m-%d') if fish.season_start else None,
            'season_end': fish.season_end.strftime('%m-%d') if fish.season_end else None,
            'is_protected': fish.is_protected,
        })
    return fish_species

def main():
    """Funcția principală de export"""
    print("🔄 Exportare date din baza de date locală...")
    
    try:
        # Exportă datele
        data = {
            'counties': export_counties(),
            'facilities': export_facilities(),
            'fish_species': export_fish_species(),
        }
        
        # Salvează în fișier JSON
        export_file = 'database_export.json'
        with open(export_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        # Statistici
        print(f"✅ Export complet salvat în: {export_file}")
        print(f"📊 Statistici:")
        print(f"   - Județe: {len(data['counties'])}")
        print(f"   - Facilități: {len(data['facilities'])}")
        print(f"   - Specii de pești: {len(data['fish_species'])}")
        
        # Afișează primele câteva înregistrări pentru verificare
        print(f"\n📋 Primele județe exportate:")
        for county in data['counties'][:5]:
            print(f"   - {county['name']} ({county['slug']})")
        
        print(f"\n🏢 Primele facilități exportate:")
        for facility in data['facilities'][:5]:
            print(f"   - {facility['name']} ({facility['icon']})")
        
        print(f"\n🐟 Primele specii exportate:")
        for fish in data['fish_species'][:5]:
            print(f"   - {fish['name']} ({fish['scientific_name']})")
        
        print(f"\n💡 Pentru import pe server, copiază fișierul {export_file} și rulează import_data.py")
        
    except Exception as e:
        print(f"❌ Eroare la export: {e}")
        return False
    
    return True

if __name__ == '__main__':
    main()
