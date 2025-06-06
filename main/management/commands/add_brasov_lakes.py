from django.core.management.base import BaseCommand
from django.utils.text import slugify
from main.models import Lake, County, FishSpecies, Facility
from decimal import Decimal


class Command(BaseCommand):
    help = 'Add fishing lakes from Brașov area to the database'

    def handle(self, *args, **options):
        self.stdout.write('Adding Brașov fishing lakes...')
        
        # Get Brașov county
        try:
            brasov_county = County.objects.get(name='Brașov')
        except County.DoesNotExist:
            self.stdout.write(self.style.ERROR('Brașov county not found. Please run populate_counties command first.'))
            return
        
        # Get Covasna county for Balta Pădureni
        try:
            covasna_county = County.objects.get(name='Covasna')
        except County.DoesNotExist:
            self.stdout.write(self.style.WARNING('Covasna county not found. Skipping Balta Pădureni.'))
            covasna_county = None

        # First, ensure we have all necessary fish species
        fish_species_to_add = [
            {'name': 'Amur', 'scientific_name': 'Ctenopharyngodon idella', 'category': 'cyprinid'},
        ]

        for fish_data in fish_species_to_add:
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

        # Ensure we have all necessary facilities
        facilities_to_add = [
            {'name': 'Foișoare', 'icon_class': 'fas fa-home', 'category': 'recreation', 'description': 'Foișoare pentru relaxare și adăpost'},
            {'name': 'Platforme betonate', 'icon_class': 'fas fa-water', 'category': 'fishing', 'description': 'Platforme betonate pentru pescuit'},
            {'name': 'Zonă de picnic', 'icon_class': 'fas fa-tree', 'category': 'recreation', 'description': 'Zonă amenajată pentru picnic'},
            {'name': 'Iluminat nocturn', 'icon_class': 'fas fa-lightbulb', 'category': 'services', 'description': 'Iluminat pentru pescuit nocturn'},
            {'name': 'Spații de grătar', 'icon_class': 'fas fa-fire', 'category': 'food', 'description': 'Spații amenajate pentru grătar'},
            {'name': 'Loc de campare', 'icon_class': 'fas fa-campground', 'category': 'accommodation', 'description': 'Zonă pentru camping'},
        ]
        
        for facility_data in facilities_to_add:
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

        # Define the lakes data
        lakes_data = [
            # Complexul Vadu Roșu
            {
                'name': 'Complexul Vadu Roșu - Balta nr. 2-3 (Doripesco)',
                'county': brasov_county,
                'description': 'Parte din renumitul complex Vadu Roșu, cunoscut pentru calitatea apei și competițiile de pescuit sportiv. Administrat de Doripesco (Delta din Carpați).',
                'address': 'Rotbav, comuna Feldioara, județul Brașov',
                'latitude': Decimal('45.6789'),  # Approximate coordinates - need to be updated
                'longitude': Decimal('25.4567'),
                'lake_type': 'competition',
                'fish_species': ['Crap', 'Caras', 'Biban', 'Șalău', 'Somn', 'Știucă'],
                'facilities': ['Platforme pescuit', 'Pontoane', 'Parcare', 'Zonă de picnic'],
                'price_per_day': Decimal('80.00'),
                'rules': 'Complex pentru competiții și pescuit sportiv. Rezervare recomandată. Program: 06:00-22:00.'
            },
            {
                'name': 'Complexul Vadu Roșu - Balta nr. 4 (Doripesco)',
                'county': brasov_county,
                'description': 'Balta principală din complexul Vadu Roșu, gazda competițiilor majore de pescuit. Aici s-au înregistrat recorduri naționale pe echipe și individual.',
                'address': 'Rotbav, comuna Feldioara, județul Brașov',
                'latitude': Decimal('45.6799'),  # Approximate coordinates - need to be updated
                'longitude': Decimal('25.4577'),
                'lake_type': 'competition',
                'fish_species': ['Crap', 'Caras', 'Biban', 'Șalău', 'Somn', 'Știucă'],
                'facilities': ['Platforme pescuit', 'Pontoane', 'Parcare', 'Zonă de picnic'],
                'price_per_day': Decimal('125.00'),  # Average of 100-150 lei
                'rules': 'Baltă pentru competiții majore. Rezervare obligatorie în sezonul de vârf (mai-septembrie). Program: 06:00-22:00.'
            },
            {
                'name': 'Complexul Vadu Roșu - Balta nr. 6 "Competitors" (Doripesco)',
                'county': brasov_county,
                'description': 'Balta intimă din complexul Vadu Roșu, ideală pentru amatori. Admite maxim 20 de pescari pe zi.',
                'address': 'Rotbav, comuna Feldioara, județul Brașov',
                'latitude': Decimal('45.6809'),  # Approximate coordinates - need to be updated
                'longitude': Decimal('25.4587'),
                'lake_type': 'private',
                'fish_species': ['Crap', 'Caras', 'Biban', 'Șalău', 'Somn', 'Știucă'],
                'facilities': ['Platforme pescuit', 'Pontoane', 'Parcare', 'Foișoare'],
                'price_per_day': Decimal('100.00'),
                'rules': 'Maxim 20 pescari/zi. Rezervare obligatorie. Ideală pentru amatori. Program: 06:00-22:00.'
            },
            
            # Baza Piscicolă Doripesco - Delta din Carpați
            {
                'name': 'Lacul Dumbrăvița (Doripesco - Delta din Carpați)',
                'county': brasov_county,
                'description': 'Parte din complexul "Delta din Carpați" cu peste 180 ha sub luciul apei. Situat la 30 km de Brașov pe drumul spre Făgăraș.',
                'address': 'Sat Dumbrăvița, comuna Feldioara, județul Brașov',
                'latitude': Decimal('45.6234'),  # Approximate coordinates - need to be updated
                'longitude': Decimal('25.3456'),
                'lake_type': 'private',
                'fish_species': ['Crap', 'Caras', 'Biban', 'Șalău', 'Avat', 'Somn'],
                'facilities': ['Pontoane', 'Spații de grătar', 'Loc de campare', 'Parcare', 'Toalete'],
                'price_per_day': Decimal('60.00'),
                'rules': 'Discounturi pentru grupuri și abonamente sezoniere. Program: 06:00-22:00.'
            },
            {
                'name': 'Balta Arini (Doripesco - Delta din Carpați)',
                'county': brasov_county,
                'description': 'Baltă din zona apropiată de Olt, lângă Dumbrăvița, cu peisaj de munte chiar lângă luciul apei.',
                'address': 'Zona Olt, lângă Dumbrăvița, județul Brașov',
                'latitude': Decimal('45.6144'),  # Approximate coordinates - need to be updated
                'longitude': Decimal('25.3366'),
                'lake_type': 'private',
                'fish_species': ['Știucă', 'Somn', 'Caras', 'Crap', 'Plătică', 'Biban'],
                'facilities': ['Platforme pescuit', 'Foișoare', 'Zonă de picnic', 'Parcare'],
                'price_per_day': Decimal('60.00'),  # Average of 50-70 lei
                'rules': 'Acces auto ușor. Tarif variabil în funcție de sezon (50-70 lei/zi). Program: 06:00-22:00.'
            },

            # Bălți în zona Belin
            {
                'name': 'Balta Nouă Belin',
                'county': brasov_county,
                'description': 'Baltă privată în satul Belin, cu maluri amenajate și facilități pentru relaxare.',
                'address': 'Belin, comuna Belin, județul Brașov',
                'latitude': Decimal('45.7123'),  # Approximate coordinates - need to be updated
                'longitude': Decimal('25.5234'),
                'lake_type': 'private',
                'fish_species': ['Biban', 'Caras', 'Crap', 'Șalău', 'Știucă', 'Somn'],
                'facilities': ['Foișoare', 'Parcare', 'Zonă de picnic'],
                'price_per_day': Decimal('40.00'),
                'rules': 'Baltă privată cu facilități pentru relaxare. Program: 06:00-22:00.'
            },
            {
                'name': 'Balta Belin Vechi',
                'county': brasov_county,
                'description': 'Baltă liniștită în localitatea Belin, ideală pentru familii și amatori. Acces auto ușor.',
                'address': 'Belin, la intrarea dinspre Măieruș, județul Brașov',
                'latitude': Decimal('45.7133'),  # Approximate coordinates - need to be updated
                'longitude': Decimal('25.5244'),
                'lake_type': 'private',
                'fish_species': ['Biban', 'Caras', 'Crap', 'Plătică', 'Roșioară', 'Somn', 'Știucă'],
                'facilities': ['Parcare', 'Zonă de picnic'],
                'price_per_day': Decimal('40.00'),
                'rules': 'Baltă liniștită, ideală pentru familii. Acces auto ușor. Program: 06:00-22:00.'
            },

            # Alte bălți din zona Brașov
            {
                'name': 'Balta Cismășu (Hărman)',
                'county': brasov_county,
                'description': 'Baltă rustică pentru pescuit recreativ în satul Hărman, la 10 km est de Brașov.',
                'address': 'Satul Hărman, comuna Hărman, județul Brașov',
                'latitude': Decimal('45.6543'),  # Approximate coordinates - need to be updated
                'longitude': Decimal('25.6789'),
                'lake_type': 'public',
                'fish_species': ['Caras', 'Crap', 'Roșioară', 'Știucă'],
                'facilities': ['Parcare'],
                'price_per_day': Decimal('5.00'),
                'rules': 'Baltă rustică cu tarif foarte accesibil. Poate deveni aglomerată în weekend. Program: 06:00-22:00.'
            },
            {
                'name': 'Balta Doripesco (Feldioara)',
                'county': brasov_county,
                'description': 'Baltă administrată de Doripesco în satul Feldioara, potrivită pentru pescuit de weekend.',
                'address': 'Sat Feldioara, comuna Feldioara, județul Brașov',
                'latitude': Decimal('45.6345'),  # Approximate coordinates - need to be updated
                'longitude': Decimal('25.4123'),
                'lake_type': 'private',
                'fish_species': ['Crap', 'Somn', 'Știucă'],
                'facilities': ['Pontoane', 'Platforme pescuit', 'Foișoare', 'Parcare'],
                'price_per_day': Decimal('65.00'),  # Average of 50-80 lei
                'rules': 'Administrat de Doripesco. Tarif variabil în funcție de perioada anului (50-80 lei/zi). Program: 06:00-22:00.'
            },
            {
                'name': 'Balta Halmeag',
                'county': brasov_county,
                'description': 'Lac de acumulare înainte de intrarea în municipiul Făgăraș, folosit frecvent de pescarii locali.',
                'address': 'Comuna Halmeag, înainte de Făgăraș, județul Brașov',
                'latitude': Decimal('45.8456'),  # Approximate coordinates - need to be updated
                'longitude': Decimal('24.9789'),
                'lake_type': 'public',
                'fish_species': ['Caras', 'Crap', 'Somn', 'Știucă'],
                'facilities': ['Parcare'],
                'price_per_day': Decimal('5.00'),  # Free to 5 lei
                'rules': 'Lac de acumulare administrat local. Acces auto facil. Tarif gratuit sau foarte mic. Program: 06:00-22:00.'
            },
            {
                'name': 'Balta Maieruș (Fântânele)',
                'county': brasov_county,
                'description': 'Baltă de interes local în satul Maieruș, preferată de pescarii pasionați de spinning.',
                'address': 'Sat Maieruș, comuna Maieruș, județul Brașov',
                'latitude': Decimal('45.7234'),  # Approximate coordinates - need to be updated
                'longitude': Decimal('25.4567'),
                'lake_type': 'public',
                'fish_species': ['Biban', 'Caras', 'Crap', 'Roșioară'],
                'facilities': [],  # No special facilities mentioned
                'price_per_day': Decimal('0.00'),  # Free
                'rules': 'Baltă gratuită de interes local. Ideală pentru spinning. Acces dinspre gară. Program liber.'
            },
            {
                'name': 'Balta Rotbav (Ansamblu 4 bălți)',
                'county': brasov_county,
                'description': 'Ansamblu de 4 bălți la circa 20 km de Brașov, pe DN13 spre Târgu Mureș, cu acces facil și facilități complete.',
                'address': 'Zona Rotbav, pe DN13 spre Târgu Mureș, județul Brașov',
                'latitude': Decimal('45.6987'),  # Approximate coordinates - need to be updated
                'longitude': Decimal('25.5123'),
                'lake_type': 'private',
                'fish_species': ['Biban', 'Caras', 'Crap', 'Somn', 'Știucă'],
                'facilities': ['Platforme betonate', 'Foișoare', 'Zonă de picnic', 'Parcare', 'Restaurant'],
                'price_per_day': Decimal('25.00'),
                'rules': 'Ansamblu de 4 bălți cu tarif unic. Acces facil de pe DN13. Restaurante în apropiere. Program: 06:00-22:00.'
            },
        ]

        # Add Covasna lake if county exists
        if covasna_county:
            lakes_data.append({
                'name': 'Balta Pădureni (Covasna - populară în Brașov)',
                'county': covasna_county,
                'description': 'Baltă în județul Covasna, foarte aproape de limita cu Brașov, populară printre pescarii din Brașov datorită apropierii și dotărilor.',
                'address': 'Comuna Moacșa, județul Covasna (aproape de limita cu Brașov)',
                'latitude': Decimal('45.7456'),  # Approximate coordinates - need to be updated
                'longitude': Decimal('25.6123'),
                'lake_type': 'public',
                'fish_species': ['Crap', 'Biban', 'Șalău', 'Știucă', 'Plătică', 'Caras', 'Roșioară'],
                'facilities': ['Parcare', 'Platforme pescuit'],
                'price_per_day': Decimal('30.00'),
                'rules': 'Repopulată periodic de Asociația Generală a Vânătorilor și Pescarilor Sportivi. Program: 06:00-22:00.'
            })

        # Add mountain and resort lakes
        mountain_resort_lakes = [
            {
                'name': 'Barajul Păltiniș',
                'county': brasov_county,
                'description': 'Lac montan lângă stațiunea Păltiniș, ideal pentru pescuitul la păstrăv. Atmosferă montană și posibilitate de pescuit la copcă iarna.',
                'address': 'Lângă stațiunea Păltiniș, zona Făgărașului, județul Brașov',
                'latitude': Decimal('45.5123'),  # Approximate coordinates - need to be updated
                'longitude': Decimal('25.1234'),
                'lake_type': 'natural',
                'fish_species': ['Păstrăv curcubeu', 'Păstrăv indigen', 'Caras', 'Plătică'],
                'facilities': ['Parcare'],
                'price_per_day': Decimal('70.00'),
                'rules': 'Pescuitul la păstrăv necesită autorizație Romsilva (≈70 lei/zi). Cote zilnice de captură strict reglementate. Acces amenajat cu poteci și scări.'
            },
            {
                'name': 'Balta Aurelia (Codlea)',
                'county': brasov_county,
                'description': 'Baltă amenajată în apropierea orașului Codlea, cu facilități complete și iluminat nocturn.',
                'address': 'În apropierea orașului Codlea, județul Brașov',
                'latitude': Decimal('45.7012'),  # Approximate coordinates - need to be updated
                'longitude': Decimal('25.4567'),
                'lake_type': 'private',
                'fish_species': ['Caras', 'Crap', 'Biban', 'Știucă', 'Șalău'],
                'facilities': ['Pontoane', 'Toalete', 'Iluminat nocturn', 'Parcare'],
                'price_per_day': Decimal('50.00'),
                'rules': 'Facilități complete cu toalete cu apă caldă și iluminat nocturn. Posibil abonamente săptămânale/lunare. Program: 06:00-22:00.'
            },
            {
                'name': 'Serenity Resort - Lacul Pescăresc (Codlea)',
                'county': brasov_county,
                'description': 'Resort cu cazare, restaurant și lac pescăresc amenajat. Facilități premium cu servicii complete de cazare și masă.',
                'address': 'Str. Halchiului nr. 100, Codlea, județul Brașov',
                'latitude': Decimal('45.7022'),  # Approximate coordinates - need to be updated
                'longitude': Decimal('25.4577'),
                'lake_type': 'private',
                'fish_species': ['Crap', 'Caras', 'Biban', 'Amur'],
                'facilities': ['Cazare', 'Restaurant', 'Foișoare', 'Iluminat nocturn', 'Pontoane', 'Parcare'],
                'price_per_day': Decimal('100.00'),  # Fishing only, packages with accommodation start at 200 lei/night
                'rules': 'Resort cu servicii complete. Pachete de pescuit cu cazare de la 200 lei/noapte (inclusiv permis). Tarif doar pescuit: 100 lei/zi. Program: 06:00-22:00.'
            },
        ]

        # Add mountain and resort lakes to the main list
        lakes_data.extend(mountain_resort_lakes)

        # Add lakes to database
        created_count = 0
        for lake_data in lakes_data:
            # Create lake
            lake, created = Lake.objects.get_or_create(
                name=lake_data['name'],
                defaults={
                    'county': lake_data['county'],
                    'description': lake_data['description'],
                    'address': lake_data['address'],
                    'latitude': lake_data['latitude'],
                    'longitude': lake_data['longitude'],
                    'lake_type': lake_data['lake_type'],
                    'price_per_day': lake_data['price_per_day'],
                    'rules': lake_data['rules'],
                    'slug': slugify(lake_data['name']),
                    'is_active': True
                }
            )
            
            if created:
                created_count += 1
                self.stdout.write(f'Created lake: {lake.name}')
                
                # Add fish species
                for fish_name in lake_data['fish_species']:
                    try:
                        fish_species = FishSpecies.objects.get(name=fish_name)
                        lake.fish_species.add(fish_species)
                    except FishSpecies.DoesNotExist:
                        self.stdout.write(f'Warning: Fish species "{fish_name}" not found')
                
                # Add facilities
                for facility_name in lake_data['facilities']:
                    try:
                        facility = Facility.objects.get(name=facility_name)
                        lake.facilities.add(facility)
                    except Facility.DoesNotExist:
                        self.stdout.write(f'Warning: Facility "{facility_name}" not found')
                
                lake.save()
            else:
                self.stdout.write(f'Lake already exists: {lake.name}')

        self.stdout.write(
            self.style.SUCCESS(f'Successfully added {created_count} lakes from Brașov area')
        )
