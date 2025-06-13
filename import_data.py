#!/usr/bin/env python
"""
Script pentru importul datelor în baza de date de producție
Importă județe, facilități și specii de pești din fișierul JSON
"""

import os
import sys
import django
import json
from pathlib import Path
from datetime import datetime

# Setup Django
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'RasfatulPescarului.settings')
django.setup()

from main.models import County, Facility, FishSpecies
from django.utils.text import slugify

def import_counties(counties_data):
    """Importă județele"""
    created_count = 0
    updated_count = 0
    
    for county_data in counties_data:
        county, created = County.objects.get_or_create(
            slug=county_data['slug'],
            defaults={
                'name': county_data['name'],
                'latitude': county_data['latitude'],
                'longitude': county_data['longitude'],
                'description': county_data['description'],
            }
        )
        
        if created:
            created_count += 1
            print(f"✅ Județ creat: {county.name}")
        else:
            # Actualizează datele existente
            county.name = county_data['name']
            county.latitude = county_data['latitude']
            county.longitude = county_data['longitude']
            county.description = county_data['description']
            county.save()
            updated_count += 1
            print(f"🔄 Județ actualizat: {county.name}")
    
    return created_count, updated_count

def import_facilities(facilities_data):
    """Importă facilitățile"""
    created_count = 0
    updated_count = 0
    
    for facility_data in facilities_data:
        facility, created = Facility.objects.get_or_create(
            name=facility_data['name'],
            defaults={
                'icon': facility_data['icon'],
                'description': facility_data['description'],
            }
        )
        
        if created:
            created_count += 1
            print(f"✅ Facilitate creată: {facility.name}")
        else:
            # Actualizează datele existente
            facility.icon = facility_data['icon']
            facility.description = facility_data['description']
            facility.save()
            updated_count += 1
            print(f"🔄 Facilitate actualizată: {facility.name}")
    
    return created_count, updated_count

def import_fish_species(fish_data):
    """Importă speciile de pești"""
    created_count = 0
    updated_count = 0
    
    for fish_species_data in fish_data:
        # Convertește datele de sezon
        season_start = None
        season_end = None
        
        if fish_species_data['season_start']:
            month, day = map(int, fish_species_data['season_start'].split('-'))
            season_start = datetime(2024, month, day).date()
        
        if fish_species_data['season_end']:
            month, day = map(int, fish_species_data['season_end'].split('-'))
            season_end = datetime(2024, month, day).date()
        
        fish, created = FishSpecies.objects.get_or_create(
            name=fish_species_data['name'],
            defaults={
                'scientific_name': fish_species_data['scientific_name'],
                'description': fish_species_data['description'],
                'min_weight': fish_species_data['min_weight'],
                'max_weight': fish_species_data['max_weight'],
                'season_start': season_start,
                'season_end': season_end,
                'is_protected': fish_species_data['is_protected'],
            }
        )
        
        if created:
            created_count += 1
            print(f"✅ Specie creată: {fish.name}")
        else:
            # Actualizează datele existente
            fish.scientific_name = fish_species_data['scientific_name']
            fish.description = fish_species_data['description']
            fish.min_weight = fish_species_data['min_weight']
            fish.max_weight = fish_species_data['max_weight']
            fish.season_start = season_start
            fish.season_end = season_end
            fish.is_protected = fish_species_data['is_protected']
            fish.save()
            updated_count += 1
            print(f"🔄 Specie actualizată: {fish.name}")
    
    return created_count, updated_count

def main():
    """Funcția principală de import"""
    import_file = 'database_export.json'
    
    if not Path(import_file).exists():
        print(f"❌ Fișierul {import_file} nu există!")
        print(f"💡 Rulează mai întâi export_data.py pe sistemul local")
        return False
    
    print(f"🔄 Importare date din {import_file}...")
    
    try:
        # Încarcă datele din JSON
        with open(import_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"📊 Date găsite:")
        print(f"   - Județe: {len(data['counties'])}")
        print(f"   - Facilități: {len(data['facilities'])}")
        print(f"   - Specii de pești: {len(data['fish_species'])}")
        print()
        
        # Importă județele
        print("🏛️  Importare județe...")
        counties_created, counties_updated = import_counties(data['counties'])
        
        # Importă facilitățile
        print("\n🏢 Importare facilități...")
        facilities_created, facilities_updated = import_facilities(data['facilities'])
        
        # Importă speciile de pești
        print("\n🐟 Importare specii de pești...")
        fish_created, fish_updated = import_fish_species(data['fish_species'])
        
        # Rezumat final
        print(f"\n🎉 Import complet!")
        print(f"📊 Rezumat:")
        print(f"   Județe: {counties_created} create, {counties_updated} actualizate")
        print(f"   Facilități: {facilities_created} create, {facilities_updated} actualizate")
        print(f"   Specii: {fish_created} create, {fish_updated} actualizate")
        
        total_created = counties_created + facilities_created + fish_created
        total_updated = counties_updated + facilities_updated + fish_updated
        print(f"\n✅ Total: {total_created} înregistrări noi, {total_updated} actualizate")
        
    except Exception as e:
        print(f"❌ Eroare la import: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == '__main__':
    main()
