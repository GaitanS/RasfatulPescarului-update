from django.db import migrations
from decimal import Decimal

def add_brasov_lakes(apps, schema_editor):
    Lake = apps.get_model('main', 'Lake')
    County = apps.get_model('main', 'County')
    
    brasov_county = County.objects.get(slug='brasov')
    
    lakes_data = [
        {
            'name': 'Balta Rotbav',
            'description': 'Complexul piscicol Rotbav este format din mai multe lacuri amenajate pentru pescuit sportiv, într-un cadru natural deosebit. Lacurile sunt populate cu diverse specii de pești și sunt întreținute regulat.',
            'address': 'Rotbav, Județul Brașov',
            'latitude': 45.8340,
            'longitude': 25.5347,
            'fish_types': 'crap, caras, șalău, știucă, plătică',
            'facilities': 'parcare camping foc grătar toalete',
            'price_per_day': Decimal('50.00'),
            'is_active': True,
            'is_featured': False
        },
        {
            'name': 'Balta Crizbav',
            'description': 'Balta Crizbav este un lac natural amenajat pentru pescuit sportiv, situat într-o zonă pitorească. Apa este curată și bogată în pește, iar facilitățile sunt moderne.',
            'address': 'Crizbav, Județul Brașov',
            'latitude': 45.8061,
            'longitude': 25.5800,
            'fish_types': 'crap crap_chinezesc caras novac',
            'facilities': 'parcare camping foc grătar toalete magazin_momeala',
            'price_per_day': Decimal('60.00'),
            'is_active': True,
            'is_featured': False
        },
        {
            'name': 'Balta Dumbravița',
            'description': 'Complex de agrement și pescuit sportiv situat la doar câțiva kilometri de Brașov. Oferă condiții excelente pentru pescuit și relaxare în natură.',
            'address': 'Dumbravița, Județul Brașov',
            'latitude': 45.7167,
            'longitude': 25.4833,
            'fish_types': 'crap caras șalău biban plătică',
            'facilities': 'parcare camping foc grătar toalete inchiriere_barci magazin_momeala',
            'price_per_day': Decimal('70.00'),
            'is_active': True,
            'is_featured': False
        },
        {
            'name': 'Balta Sânpetru',
            'description': 'Balta de pescuit din Sânpetru este un loc perfect pentru pescarii începători și experimentați. Lacul este bine populat și întreținut cu grijă.',
            'address': 'Sânpetru, Județul Brașov',
            'latitude': 45.7000,
            'longitude': 25.6667,
            'fish_types': 'crap caras novac șalău',
            'facilities': 'parcare toalete foc grătar',
            'price_per_day': Decimal('45.00'),
            'is_active': True,
            'is_featured': False
        },
        {
            'name': 'Balta Prejmer',
            'description': 'Complexul piscicol Prejmer oferă mai multe lacuri pentru pescuit sportiv, cu o suprafață totală de peste 20 de hectare. Locul ideal pentru o zi de pescuit în natură.',
            'address': 'Prejmer, Județul Brașov',
            'latitude': 45.7333,
            'longitude': 25.7667,
            'fish_types': 'crap caras novac șalău știucă biban',
            'facilities': 'parcare camping foc grătar toalete inchiriere_barci magazin_momeala',
            'price_per_day': Decimal('65.00'),
            'is_active': True,
            'is_featured': False
        }
    ]
    
    for lake_data in lakes_data:
        Lake.objects.get_or_create(
            name=lake_data['name'],
            county=brasov_county,
            defaults=lake_data
        )

class Migration(migrations.Migration):
    dependencies = [
        ('main', '0024_lake_model'),
    ]

    operations = [
        migrations.RunPython(add_brasov_lakes),
    ]