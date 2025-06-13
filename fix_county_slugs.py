#!/usr/bin/env python
"""
Script pentru corectarea slug-urilor județelor
Rezolvă problema cu NoReverseMatch pentru județele cu spații în nume
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

def fix_county_slugs():
    """Corectează slug-urile pentru județele cu spații și caractere speciale"""
    print("🔧 Corectare slug-uri județe...")
    
    # Județele care pot avea probleme cu slug-urile
    problematic_counties = [
        'Satu Mare', 'Bistrița-Năsăud', 'Caraș-Severin'
    ]
    
    fixed_count = 0
    
    # Verifică toate județele
    for county in County.objects.all():
        old_slug = getattr(county, 'slug', None) if hasattr(county, 'slug') else None
        
        # Generează slug corect
        correct_slug = slugify(county.name, allow_unicode=False)
        
        # Verifică dacă trebuie actualizat
        needs_update = False
        
        if hasattr(county, 'slug'):
            if county.slug != correct_slug:
                needs_update = True
                print(f"🔄 {county.name}: '{county.slug}' -> '{correct_slug}'")
        else:
            print(f"⚠️  {county.name}: Câmpul slug nu există în model")
            continue
        
        # Actualizează dacă e necesar
        if needs_update:
            try:
                county.slug = correct_slug
                county.save()
                print(f"✅ Actualizat: {county.name}")
                fixed_count += 1
            except Exception as e:
                print(f"❌ Eroare la {county.name}: {e}")
    
    print(f"\n📊 Rezultat:")
    print(f"   - Județe corectate: {fixed_count}")
    print(f"   - Total județe: {County.objects.count()}")
    
    return fixed_count > 0

def verify_slugs():
    """Verifică că toate slug-urile sunt corecte"""
    print("\n🔍 Verificare slug-uri...")
    
    for county in County.objects.all():
        if hasattr(county, 'slug'):
            expected_slug = slugify(county.name, allow_unicode=False)
            if county.slug == expected_slug:
                print(f"✅ {county.name} -> {county.slug}")
            else:
                print(f"❌ {county.name}: '{county.slug}' != '{expected_slug}'")
        else:
            print(f"⚠️  {county.name}: Fără slug")

def recreate_counties_with_slugs():
    """Recreează toate județele cu slug-uri corecte"""
    print("🔄 Recreare județe cu slug-uri corecte...")
    
    # Lista completă a județelor
    counties = [
        'Alba', 'Arad', 'Argeș', 'Bacău', 'Bihor', 'Bistrița-Năsăud', 'Botoșani',
        'Brașov', 'Brăila', 'Buzău', 'Caraș-Severin', 'Călărași', 'Cluj', 'Constanța',
        'Covasna', 'Dâmbovița', 'Dolj', 'Galați', 'Giurgiu', 'Gorj', 'Harghita',
        'Hunedoara', 'Ialomița', 'Iași', 'Ilfov', 'Maramureș', 'Mehedinți', 'Mureș',
        'Neamț', 'Olt', 'Prahova', 'Satu Mare', 'Sălaj', 'Sibiu', 'Suceava',
        'Teleorman', 'Timiș', 'Tulcea', 'Vaslui', 'Vâlcea', 'Vrancea', 'București'
    ]
    
    # Șterge județele existente
    County.objects.all().delete()
    print("🗑️  Județe existente șterse")
    
    created_count = 0
    
    for county_name in counties:
        slug = slugify(county_name, allow_unicode=False)
        
        try:
            # Încearcă să creeze cu slug
            if hasattr(County, 'slug'):
                county = County.objects.create(name=county_name, slug=slug)
                print(f"✅ {county_name} -> {slug}")
            else:
                county = County.objects.create(name=county_name)
                print(f"✅ {county_name} (fără slug)")
            created_count += 1
        except Exception as e:
            print(f"❌ {county_name}: {e}")
    
    print(f"\n📊 Rezultat:")
    print(f"   - Județe create: {created_count}")
    print(f"   - Total județe: {County.objects.count()}")

if __name__ == '__main__':
    print("🏛️  Fix County Slugs - Răsfățul Pescarului")
    print("=" * 50)
    
    # Verifică dacă există județe
    if not County.objects.exists():
        print("⚠️  Nu există județe în baza de date!")
        print("💡 Rulează mai întâi scriptul pentru adăugarea județelor")
        sys.exit(1)
    
    # Verifică structura modelului
    has_slug_field = hasattr(County, 'slug')
    print(f"📋 Model County are câmpul slug: {'✅' if has_slug_field else '❌'}")
    
    if not has_slug_field:
        print("⚠️  Modelul County nu are câmpul slug!")
        print("💡 Adaugă câmpul slug în model și rulează migrațiile")
        sys.exit(1)
    
    # Încearcă să corecteze slug-urile existente
    if fix_county_slugs():
        print("\n🎉 Slug-urile au fost corectate!")
    else:
        print("\n✅ Toate slug-urile sunt deja corecte!")
    
    # Verifică rezultatul
    verify_slugs()
