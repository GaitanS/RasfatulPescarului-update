#!/usr/bin/env python
"""
Script pentru adăugarea județelor cu slug-uri corecte
Versiune actualizată care rezolvă problema NoReverseMatch
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

from main.models import County
from django.utils.text import slugify

# Lista completă a județelor României
counties = [
    'Alba', 'Arad', 'Argeș', 'Bacău', 'Bihor', 'Bistrița-Năsăud', 'Botoșani',
    'Brașov', 'Brăila', 'Buzău', 'Caraș-Severin', 'Călărași', 'Cluj', 'Constanța',
    'Covasna', 'Dâmbovița', 'Dolj', 'Galați', 'Giurgiu', 'Gorj', 'Harghita',
    'Hunedoara', 'Ialomița', 'Iași', 'Ilfov', 'Maramureș', 'Mehedinți', 'Mureș',
    'Neamț', 'Olt', 'Prahova', 'Satu Mare', 'Sălaj', 'Sibiu', 'Suceava',
    'Teleorman', 'Timiș', 'Tulcea', 'Vaslui', 'Vâlcea', 'Vrancea', 'București'
]

def add_counties():
    """Adaugă toate județele în baza de date cu slug-uri corecte"""
    added_count = 0
    existing_count = 0
    
    print("🏛️  Adăugare județe cu slug-uri corecte...")
    
    for county_name in counties:
        # Generează slug corect folosind Django's slugify
        correct_slug = slugify(county_name, allow_unicode=False)
        
        # Încearcă să creeze județul cu slug corect
        try:
            if hasattr(County, 'slug'):
                county, created = County.objects.get_or_create(
                    name=county_name,
                    defaults={'slug': correct_slug}
                )
                
                # Dacă există dar are slug greșit, actualizează-l
                if not created and county.slug != correct_slug:
                    old_slug = county.slug
                    county.slug = correct_slug
                    county.save()
                    print(f"🔄 Actualizat slug: {county_name} ('{old_slug}' -> '{correct_slug}')")
                    
            else:
                county, created = County.objects.get_or_create(name=county_name)
                print(f"⚠️  {county_name} - câmpul slug nu există în model")
                
        except Exception as e:
            print(f"❌ Eroare la {county_name}: {e}")
            continue
        
        if created:
            print(f"✅ Adăugat: {county_name} -> {correct_slug}")
            added_count += 1
        else:
            if hasattr(County, 'slug'):
                print(f"⚠️  Există deja: {county_name} -> {county.slug}")
            else:
                print(f"⚠️  Există deja: {county_name}")
            existing_count += 1
    
    print(f"\n📊 Rezultat:")
    print(f"   - Județe adăugate: {added_count}")
    print(f"   - Județe existente: {existing_count}")
    print(f"   - Total județe: {County.objects.count()}")

def verify_slugs():
    """Verifică că toate slug-urile sunt corecte"""
    print("\n🔍 Verificare slug-uri...")
    
    problematic_slugs = []
    
    for county in County.objects.all():
        if hasattr(county, 'slug'):
            expected_slug = slugify(county.name, allow_unicode=False)
            if county.slug == expected_slug:
                print(f"✅ {county.name} -> {county.slug}")
            else:
                print(f"❌ {county.name}: '{county.slug}' != '{expected_slug}'")
                problematic_slugs.append(county)
        else:
            print(f"⚠️  {county.name}: Fără câmp slug")
    
    if problematic_slugs:
        print(f"\n⚠️  {len(problematic_slugs)} județe cu slug-uri problematice!")
        return False
    else:
        print("\n✅ Toate slug-urile sunt corecte!")
        return True

def show_examples():
    """Afișează exemple de slug-uri pentru județele problematice"""
    print("\n📝 Exemple de slug-uri corecte:")
    examples = ['Satu Mare', 'Bistrița-Năsăud', 'Caraș-Severin']
    
    for name in examples:
        slug = slugify(name, allow_unicode=False)
        print(f"   {name} -> {slug}")

if __name__ == '__main__':
    print("🏛️  Add Counties (Fixed) - Răsfățul Pescarului")
    print("=" * 50)
    
    # Verifică dacă modelul are câmpul slug
    has_slug_field = hasattr(County, 'slug')
    print(f"📋 Model County are câmpul slug: {'✅' if has_slug_field else '❌'}")
    
    if not has_slug_field:
        print("⚠️  ATENȚIE: Modelul County nu are câmpul slug!")
        print("💡 Județele vor fi adăugate doar cu câmpul name")
        print("💡 Pentru slug-uri, adaugă câmpul în model și rulează migrațiile")
    
    # Afișează exemple
    show_examples()
    
    # Adaugă județele
    add_counties()
    
    # Verifică rezultatul
    if has_slug_field:
        verify_slugs()
    
    print("\n🎉 Finalizat!")
