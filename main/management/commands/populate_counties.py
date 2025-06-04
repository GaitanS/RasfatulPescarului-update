import logging
from django.core.management.base import BaseCommand
from main.models import County

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Populează baza de date cu toate județele din România'

    def handle(self, *args, **options):
        # Lista județelor din România cu regiunile corespunzătoare
        counties = [
            # Moldova
            {'name': 'Bacău', 'region': 'MOLDOVA'},
            {'name': 'Botoșani', 'region': 'MOLDOVA'},
            {'name': 'Iași', 'region': 'MOLDOVA'},
            {'name': 'Neamț', 'region': 'MOLDOVA'},
            {'name': 'Suceava', 'region': 'MOLDOVA'},
            {'name': 'Vaslui', 'region': 'MOLDOVA'},
            {'name': 'Galați', 'region': 'MOLDOVA'},
            {'name': 'Vrancea', 'region': 'MOLDOVA'},
            
            # Muntenia
            {'name': 'Argeș', 'region': 'MUNTENIA'},
            {'name': 'Călărași', 'region': 'MUNTENIA'},
            {'name': 'Dâmbovița', 'region': 'MUNTENIA'},
            {'name': 'Giurgiu', 'region': 'MUNTENIA'},
            {'name': 'Ialomița', 'region': 'MUNTENIA'},
            {'name': 'Prahova', 'region': 'MUNTENIA'},
            {'name': 'Teleorman', 'region': 'MUNTENIA'},
            
            # Oltenia
            {'name': 'Dolj', 'region': 'OLTENIA'},
            {'name': 'Gorj', 'region': 'OLTENIA'},
            {'name': 'Mehedinți', 'region': 'OLTENIA'},
            {'name': 'Olt', 'region': 'OLTENIA'},
            {'name': 'Vâlcea', 'region': 'OLTENIA'},
            
            # Banat
            {'name': 'Arad', 'region': 'BANAT'},
            {'name': 'Caraș-Severin', 'region': 'BANAT'},
            {'name': 'Timiș', 'region': 'BANAT'},
            
            # Crișana
            {'name': 'Bihor', 'region': 'CRISANA'},
            {'name': 'Satu Mare', 'region': 'CRISANA'},
            
            # Maramureș
            {'name': 'Maramureș', 'region': 'MARAMURES'},
            
            # Transilvania
            {'name': 'Alba', 'region': 'TRANSILVANIA'},
            {'name': 'Bistrița-Năsăud', 'region': 'TRANSILVANIA'},
            {'name': 'Brașov', 'region': 'TRANSILVANIA'},
            {'name': 'Cluj', 'region': 'TRANSILVANIA'},
            {'name': 'Covasna', 'region': 'TRANSILVANIA'},
            {'name': 'Harghita', 'region': 'TRANSILVANIA'},
            {'name': 'Hunedoara', 'region': 'TRANSILVANIA'},
            {'name': 'Mureș', 'region': 'TRANSILVANIA'},
            {'name': 'Sălaj', 'region': 'TRANSILVANIA'},
            {'name': 'Sibiu', 'region': 'TRANSILVANIA'},
            
            # Dobrogea
            {'name': 'Constanța', 'region': 'DOBROGEA'},
            {'name': 'Tulcea', 'region': 'DOBROGEA'},
            
            # București
            {'name': 'București', 'region': 'BUCURESTI'},
            {'name': 'Ilfov', 'region': 'BUCURESTI'},
        ]
        
        # Contorizare județe adăugate și actualizate
        created_count = 0
        updated_count = 0
        
        for county_data in counties:
            county, created = County.objects.update_or_create(
                name=county_data['name'],
                defaults={'region': county_data['region']}
            )
            
            if created:
                created_count += 1
            else:
                updated_count += 1
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Populare completă: {created_count} județe create, {updated_count} județe actualizate'
            )
        )