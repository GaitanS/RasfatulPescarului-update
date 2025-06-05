from django.core.management.base import BaseCommand
from main.models import FishSpecies, Facility


class Command(BaseCommand):
    help = 'Populate database with initial fish species and facilities'

    def handle(self, *args, **options):
        self.stdout.write('Populating fish species...')
        
        # Fish species data
        fish_species_data = [
            # Cyprinids (Ciprinide)
            {'name': 'Crap', 'scientific_name': 'Cyprinus carpio', 'category': 'cyprinid'},
            {'name': 'Caras', 'scientific_name': 'Carassius carassius', 'category': 'cyprinid'},
            {'name': 'Caras argintiu', 'scientific_name': 'Carassius gibelio', 'category': 'cyprinid'},
            {'name': 'Roșioară', 'scientific_name': 'Rutilus rutilus', 'category': 'cyprinid'},
            {'name': 'Clean', 'scientific_name': 'Leuciscus cephalus', 'category': 'cyprinid'},
            {'name': 'Plătică', 'scientific_name': 'Abramis brama', 'category': 'cyprinid'},
            {'name': 'Babușcă', 'scientific_name': 'Barbus barbus', 'category': 'cyprinid'},
            {'name': 'Văduvă', 'scientific_name': 'Leuciscus idus', 'category': 'cyprinid'},
            {'name': 'Boarță', 'scientific_name': 'Chondrostoma nasus', 'category': 'cyprinid'},
            {'name': 'Linul', 'scientific_name': 'Tinca tinca', 'category': 'cyprinid'},
            
            # Predators (Prădători)
            {'name': 'Șalău', 'scientific_name': 'Sander lucioperca', 'category': 'predator'},
            {'name': 'Știucă', 'scientific_name': 'Esox lucius', 'category': 'predator'},
            {'name': 'Biban', 'scientific_name': 'Perca fluviatilis', 'category': 'predator'},
            {'name': 'Somn', 'scientific_name': 'Silurus glanis', 'category': 'predator'},
            {'name': 'Somn pitic', 'scientific_name': 'Ictalurus nebulosus', 'category': 'predator'},
            {'name': 'Păstrăv curcubeu', 'scientific_name': 'Oncorhynchus mykiss', 'category': 'predator'},
            {'name': 'Păstrăv indigen', 'scientific_name': 'Salmo trutta fario', 'category': 'predator'},
            
            # Other species (Alte specii)
            {'name': 'Morunaș', 'scientific_name': 'Hucho hucho', 'category': 'other'},
            {'name': 'Obleț', 'scientific_name': 'Alburnus alburnus', 'category': 'other'},
            {'name': 'Scobarul', 'scientific_name': 'Gymnocephalus cernua', 'category': 'other'},
            {'name': 'Țipar', 'scientific_name': 'Aspius aspius', 'category': 'other'},
            {'name': 'Avat', 'scientific_name': 'Thymallus thymallus', 'category': 'other'},
            {'name': 'Mreană', 'scientific_name': 'Barbus meridionalis', 'category': 'other'},
        ]
        
        for fish_data in fish_species_data:
            fish_species, created = FishSpecies.objects.get_or_create(
                name=fish_data['name'],
                defaults={
                    'scientific_name': fish_data['scientific_name'],
                    'category': fish_data['category'],
                    'is_active': True
                }
            )
            if created:
                self.stdout.write(f'Created fish species: {fish_species.name}')
            else:
                self.stdout.write(f'Fish species already exists: {fish_species.name}')
        
        self.stdout.write('Populating facilities...')
        
        # Facilities data
        facilities_data = [
            # Basic (De bază)
            {'name': 'Parcare', 'icon_class': 'fas fa-parking', 'category': 'basic', 'description': 'Loc de parcare pentru autoturisme'},
            {'name': 'Toalete', 'icon_class': 'fas fa-restroom', 'category': 'basic', 'description': 'Toalete publice'},
            {'name': 'Apă potabilă', 'icon_class': 'fas fa-tint', 'category': 'basic', 'description': 'Acces la apă potabilă'},
            {'name': 'Gunoi/Reciclare', 'icon_class': 'fas fa-recycle', 'category': 'basic', 'description': 'Containere pentru gunoi și reciclare'},
            
            # Accommodation (Cazare)
            {'name': 'Cazare', 'icon_class': 'fas fa-bed', 'category': 'accommodation', 'description': 'Camere de cazare disponibile'},
            {'name': 'Camping', 'icon_class': 'fas fa-campground', 'category': 'accommodation', 'description': 'Zonă de camping amenajată'},
            {'name': 'Cabane', 'icon_class': 'fas fa-home', 'category': 'accommodation', 'description': 'Cabane pentru cazare'},
            {'name': 'Corturi', 'icon_class': 'fas fa-tent', 'category': 'accommodation', 'description': 'Zonă pentru corturi'},
            
            # Food & Drink (Mâncare și băutură)
            {'name': 'Restaurant', 'icon_class': 'fas fa-utensils', 'category': 'food', 'description': 'Restaurant cu servicii complete'},
            {'name': 'Bar', 'icon_class': 'fas fa-cocktail', 'category': 'food', 'description': 'Bar cu băuturi'},
            {'name': 'Bufet', 'icon_class': 'fas fa-hamburger', 'category': 'food', 'description': 'Bufet cu mâncare rapidă'},
            {'name': 'Grătar', 'icon_class': 'fas fa-fire', 'category': 'food', 'description': 'Zonă de grătar amenajată'},
            {'name': 'Bucătărie comună', 'icon_class': 'fas fa-kitchen-set', 'category': 'food', 'description': 'Bucătărie comună pentru oaspeți'},
            
            # Fishing (Pescuit)
            {'name': 'Magazin pescuit', 'icon_class': 'fas fa-store', 'category': 'fishing', 'description': 'Magazin cu echipamente de pescuit'},
            {'name': 'Închiriere echipamente', 'icon_class': 'fas fa-tools', 'category': 'fishing', 'description': 'Închiriere echipamente de pescuit'},
            {'name': 'Pontoane', 'icon_class': 'fas fa-ship', 'category': 'fishing', 'description': 'Pontoane pentru pescuit'},
            {'name': 'Platforme pescuit', 'icon_class': 'fas fa-water', 'category': 'fishing', 'description': 'Platforme amenajate pentru pescuit'},
            {'name': 'Depozit echipamente', 'icon_class': 'fas fa-warehouse', 'category': 'fishing', 'description': 'Depozit pentru echipamente personale'},
            
            # Services (Servicii)
            {'name': 'WiFi', 'icon_class': 'fas fa-wifi', 'category': 'services', 'description': 'Internet wireless gratuit'},
            {'name': 'Electricitate', 'icon_class': 'fas fa-plug', 'category': 'services', 'description': 'Prize electrice disponibile'},
            {'name': 'Duș', 'icon_class': 'fas fa-shower', 'category': 'services', 'description': 'Dușuri cu apă caldă'},
            {'name': 'Spălătorie', 'icon_class': 'fas fa-tshirt', 'category': 'services', 'description': 'Servicii de spălătorie'},
            {'name': 'Primul ajutor', 'icon_class': 'fas fa-first-aid', 'category': 'services', 'description': 'Kit de primul ajutor disponibil'},
            
            # Recreation (Recreere)
            {'name': 'Teren de joacă', 'icon_class': 'fas fa-child', 'category': 'recreation', 'description': 'Teren de joacă pentru copii'},
            {'name': 'Teren sport', 'icon_class': 'fas fa-futbol', 'category': 'recreation', 'description': 'Teren pentru activități sportive'},
            {'name': 'Piscină', 'icon_class': 'fas fa-swimming-pool', 'category': 'recreation', 'description': 'Piscină pentru înot'},
            {'name': 'Plajă', 'icon_class': 'fas fa-umbrella-beach', 'category': 'recreation', 'description': 'Zonă de plajă amenajată'},
        ]
        
        for facility_data in facilities_data:
            facility, created = Facility.objects.get_or_create(
                name=facility_data['name'],
                defaults={
                    'icon_class': facility_data['icon_class'],
                    'category': facility_data['category'],
                    'description': facility_data['description'],
                    'is_active': True
                }
            )
            if created:
                self.stdout.write(f'Created facility: {facility.name}')
            else:
                self.stdout.write(f'Facility already exists: {facility.name}')
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully populated {FishSpecies.objects.count()} fish species and {Facility.objects.count()} facilities'
            )
        )
