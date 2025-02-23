from django.db import migrations

def add_counties_data(apps, schema_editor):
    County = apps.get_model('main', 'County')
    
    # List of Romanian counties with their regions
    counties_data = [
        # Moldova Region
        {'name': 'Bacău', 'slug': 'bacau', 'region': 'Moldova'},
        {'name': 'Botoșani', 'slug': 'botosani', 'region': 'Moldova'},
        {'name': 'Iași', 'slug': 'iasi', 'region': 'Moldova'},
        {'name': 'Neamț', 'slug': 'neamt', 'region': 'Moldova'},
        {'name': 'Suceava', 'slug': 'suceava', 'region': 'Moldova'},
        {'name': 'Vaslui', 'slug': 'vaslui', 'region': 'Moldova'},
        {'name': 'Galați', 'slug': 'galati', 'region': 'Moldova'},
        {'name': 'Vrancea', 'slug': 'vrancea', 'region': 'Moldova'},
        
        # Muntenia Region
        {'name': 'Argeș', 'slug': 'arges', 'region': 'Muntenia'},
        {'name': 'Călărași', 'slug': 'calarasi', 'region': 'Muntenia'},
        {'name': 'Dâmbovița', 'slug': 'dambovita', 'region': 'Muntenia'},
        {'name': 'Giurgiu', 'slug': 'giurgiu', 'region': 'Muntenia'},
        {'name': 'Ialomița', 'slug': 'ialomita', 'region': 'Muntenia'},
        {'name': 'Prahova', 'slug': 'prahova', 'region': 'Muntenia'},
        {'name': 'Teleorman', 'slug': 'teleorman', 'region': 'Muntenia'},
        
        # Dobrogea Region
        {'name': 'Constanța', 'slug': 'constanta', 'region': 'Dobrogea'},
        {'name': 'Tulcea', 'slug': 'tulcea', 'region': 'Dobrogea'},
        
        # Transilvania Region
        {'name': 'Alba', 'slug': 'alba', 'region': 'Transilvania'},
        {'name': 'Bistrița-Năsăud', 'slug': 'bistrita-nasaud', 'region': 'Transilvania'},
        {'name': 'Brașov', 'slug': 'brasov', 'region': 'Transilvania'},
        {'name': 'Cluj', 'slug': 'cluj', 'region': 'Transilvania'},
        {'name': 'Covasna', 'slug': 'covasna', 'region': 'Transilvania'},
        {'name': 'Harghita', 'slug': 'harghita', 'region': 'Transilvania'},
        {'name': 'Hunedoara', 'slug': 'hunedoara', 'region': 'Transilvania'},
        {'name': 'Mureș', 'slug': 'mures', 'region': 'Transilvania'},
        {'name': 'Sibiu', 'slug': 'sibiu', 'region': 'Transilvania'},
        
        # Maramureș Region
        {'name': 'Maramureș', 'slug': 'maramures', 'region': 'Maramureș'},
        {'name': 'Satu Mare', 'slug': 'satu-mare', 'region': 'Maramureș'},
        
        # Crișana Region
        {'name': 'Arad', 'slug': 'arad', 'region': 'Crișana'},
        {'name': 'Bihor', 'slug': 'bihor', 'region': 'Crișana'},
        
        # Banat Region
        {'name': 'Caraș-Severin', 'slug': 'caras-severin', 'region': 'Banat'},
        {'name': 'Timiș', 'slug': 'timis', 'region': 'Banat'},
        
        # Oltenia Region
        {'name': 'Dolj', 'slug': 'dolj', 'region': 'Oltenia'},
        {'name': 'Gorj', 'slug': 'gorj', 'region': 'Oltenia'},
        {'name': 'Mehedinți', 'slug': 'mehedinti', 'region': 'Oltenia'},
        {'name': 'Olt', 'slug': 'olt', 'region': 'Oltenia'},
        {'name': 'Vâlcea', 'slug': 'valcea', 'region': 'Oltenia'},
        
        # București-Ilfov Region
        {'name': 'București', 'slug': 'bucuresti', 'region': 'București-Ilfov'},
        {'name': 'Ilfov', 'slug': 'ilfov', 'region': 'București-Ilfov'},
        
        # Bucovina Region (part of historical region)
        {'name': 'Brăila', 'slug': 'braila', 'region': 'Muntenia'},
        {'name': 'Buzău', 'slug': 'buzau', 'region': 'Muntenia'},
    ]
    
    for county_data in counties_data:
        County.objects.get_or_create(
            name=county_data['name'],
            defaults={
                'slug': county_data['slug'],
                'region': county_data['region']
            }
        )

class Migration(migrations.Migration):
    dependencies = [
        ('main', '0023_remove_lake_county_remove_order_county_and_more'),
    ]

    operations = [
        migrations.RunPython(add_counties_data),
    ]