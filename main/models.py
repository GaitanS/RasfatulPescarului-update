from django.db import models
from django.utils.text import slugify
from django.utils.safestring import mark_safe
from django.core.validators import MinLengthValidator, MaxValueValidator, MinValueValidator
from django.db.models import Avg, Count
import re

class FishSpecies(models.Model):
    CATEGORY_CHOICES = [
        ('cyprinid', 'Ciprinide'),
        ('predator', 'Prădători'),
        ('other', 'Alte specii'),
    ]

    name = models.CharField(
        max_length=100,
        verbose_name="Numele speciei",
        help_text="Numele românesc al speciei de pește"
    )
    scientific_name = models.CharField(
        max_length=150,
        blank=True,
        verbose_name="Numele științific",
        help_text="Numele latin al speciei (opțional)"
    )
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='other',
        verbose_name="Categoria",
        help_text="Categoria biologică a peștelui"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Activ"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data creării")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Data actualizării")

    class Meta:
        verbose_name = "Specie de pește"
        verbose_name_plural = "Specii de pești"
        ordering = ['category', 'name']

    def __str__(self):
        return self.name

class Facility(models.Model):
    CATEGORY_CHOICES = [
        ('basic', 'De bază'),
        ('accommodation', 'Cazare'),
        ('food', 'Mâncare și băutură'),
        ('fishing', 'Pescuit'),
        ('services', 'Servicii'),
        ('recreation', 'Recreere'),
    ]

    name = models.CharField(
        max_length=100,
        verbose_name="Numele facilității"
    )
    icon_class = models.CharField(
        max_length=50,
        verbose_name="Clasa icon FontAwesome",
        help_text="Ex: fas fa-parking, fas fa-bed"
    )
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='basic',
        verbose_name="Categoria"
    )
    description = models.TextField(
        blank=True,
        verbose_name="Descriere",
        help_text="Descrierea detaliată a facilității"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Activ"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data creării")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Data actualizării")

    class Meta:
        verbose_name = "Facilitate"
        verbose_name_plural = "Facilități"
        ordering = ['category', 'name']

    def __str__(self):
        return self.name

    def get_category_display_romanian(self):
        """Return Romanian category name for admin display"""
        category_map = {
            'basic': 'De bază',
            'accommodation': 'Cazare',
            'food': 'Mâncare și băutură',
            'fishing': 'Pescuit',
            'services': 'Servicii',
            'recreation': 'Recreere',
        }
        return category_map.get(self.category, self.category)

class County(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="Nume județ",
        help_text="Numele complet al județului (ex: Argeș, Brașov, Cluj)"
    )
    slug = models.SlugField(
        max_length=100,
        unique=True,
        verbose_name="URL slug",
        help_text="Se generează automat din nume. Folosit pentru URL-uri (ex: arges, brasov)"
    )
    region = models.CharField(
        max_length=50,
        choices=[
            ('MOLDOVA', 'Moldova'),
            ('MUNTENIA', 'Muntenia'),
            ('OLTENIA', 'Oltenia'),
            ('BANAT', 'Banat'),
            ('CRISANA', 'Crișana'),
            ('MARAMURES', 'Maramureș'),
            ('TRANSILVANIA', 'Transilvania'),
            ('DOBROGEA', 'Dobrogea'),
            ('BUCURESTI', 'București')
        ],
        verbose_name="Regiune",
        help_text="Regiunea istorică din care face parte județul"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data creării")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Data actualizării")

    class Meta:
        verbose_name = "Județ"
        verbose_name_plural = "Județe"
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class SiteSettings(models.Model):
    site_name = models.CharField(
        max_length=100,
        default='Răsfățul Pescarului',
        verbose_name="Numele site-ului",
        help_text="Numele principal al site-ului care apare în titlu și logo"
    )
    contact_email = models.EmailField(
        default='contact@rasfatulpescarului.ro',
        verbose_name="Email de contact",
        help_text="Adresa de email principală pentru contact (ex: contact@site.ro)"
    )
    phone = models.CharField(
        max_length=20,
        default='0700000000',
        verbose_name="Număr de telefon",
        help_text="Numărul de telefon pentru contact (ex: 0700 123 456)"
    )
    address = models.TextField(
        default='România',
        verbose_name="Adresa",
        help_text="Adresa completă a companiei"
    )
    facebook_url = models.URLField(
        blank=True,
        verbose_name="Link Facebook",
        help_text="URL-ul complet către pagina de Facebook (ex: https://facebook.com/pagina)"
    )
    instagram_url = models.URLField(
        blank=True,
        verbose_name="Link Instagram",
        help_text="URL-ul complet către pagina de Instagram"
    )
    youtube_url = models.URLField(
        blank=True,
        verbose_name="Link YouTube",
        help_text="URL-ul complet către canalul de YouTube"
    )
    about_text = models.TextField(
        default='Despre noi',
        verbose_name="Text despre noi",
        help_text="Descrierea scurtă a companiei care apare în footer"
    )

    class Meta:
        verbose_name = 'Setări Site'
        verbose_name_plural = 'Setări Site'

    def __str__(self):
        return self.site_name

    @classmethod
    def get_settings(cls):
        return cls.objects.first()

class FooterSettings(models.Model):
    contact_info = models.CharField(
        max_length=200,
        default='Contact',
        verbose_name="Informații contact",
        help_text="Titlul secțiunii de contact din footer"
    )
    address = models.TextField(
        default='Strada Exemplu, Nr. 123, București',
        verbose_name="Adresa completă",
        help_text="Adresa fizică completă care apare în footer"
    )
    phone = models.CharField(
        max_length=20,
        default='+40 123 456 789',
        verbose_name="Telefon",
        help_text="Numărul de telefon cu prefixul țării (ex: +40 123 456 789)"
    )
    email = models.EmailField(
        default='contact@rasfatulpescarului.ro',
        verbose_name="Email",
        help_text="Adresa de email care apare în footer"
    )
    working_hours = models.CharField(
        max_length=100,
        default='Luni - Vineri: 09:00 - 18:00',
        verbose_name="Program de lucru",
        help_text="Programul de lucru (ex: Luni - Vineri: 09:00 - 18:00)"
    )

    class Meta:
        verbose_name = 'Setări Footer'
        verbose_name_plural = 'Setări Footer'

    def __str__(self):
        return 'Footer Settings'

    @classmethod
    def get_settings(cls):
        return cls.objects.first()

class Lake(models.Model):
    LAKE_TYPE_CHOICES = [
        ('private', 'Baltă privată'),
        ('public', 'Baltă publică'),
        ('competition', 'Baltă pentru competiții'),
        ('catch_release', 'Baltă cu regim "catch & release"'),
        ('mixed', 'Baltă cu regim mixt (reținere + catch & release)'),
        ('natural', 'Baltă naturală'),
    ]

    name = models.CharField(
        max_length=200,
        verbose_name="Numele lacului",
        help_text="Numele complet al lacului sau bălții de pescuit"
    )
    slug = models.SlugField(
        max_length=250,
        unique=True,
        verbose_name="URL slug",
        help_text="URL-ul prietenos pentru lac (se generează automat din nume)"
    )
    description = models.TextField(
        blank=True,
        verbose_name="Descriere",
        help_text="Descrierea detaliată a lacului, facilităților și condițiilor de pescuit"
    )
    address = models.CharField(
        max_length=255,
        verbose_name="Adresa",
        help_text="Adresa completă a lacului (ex: Comuna X, Județul Y)"
    )
    county = models.ForeignKey(
        County,
        on_delete=models.CASCADE,
        related_name='lakes',
        verbose_name="Județul",
        help_text="Județul în care se află lacul"
    )
    latitude = models.DecimalField(
        max_digits=18,
        decimal_places=15,
        verbose_name="Latitudine",
        help_text="Coordonata latitudine cu precizie mare (ex: 45.39189813235069). Folosește Google Maps pentru a găsi coordonatele"
    )
    longitude = models.DecimalField(
        max_digits=18,
        decimal_places=15,
        verbose_name="Longitudine",
        help_text="Coordonata longitudine cu precizie mare (ex: 24.62707585690222). Folosește Google Maps pentru a găsi coordonatele"
    )
    google_maps_embed = models.TextField(
        blank=True,
        null=True,
        verbose_name="Cod embed Google Maps",
        help_text="Cod iframe complet de la Google Maps (opțional). Dacă este completat, va fi folosit în locul coordonatelor. Exemplu: <iframe src='...' width='600' height='450'></iframe>"
    )
    lake_type = models.CharField(
        max_length=50,
        choices=LAKE_TYPE_CHOICES,
        default='private',
        verbose_name="Tipul bălții",
        help_text="Selectează tipul de baltă în funcție de administrare și regulament"
    )
    fish_species = models.ManyToManyField(
        FishSpecies,
        blank=True,
        verbose_name="Specii de pești",
        help_text="Selectează speciile de pești disponibile în acest lac"
    )
    facilities = models.ManyToManyField(
        Facility,
        blank=True,
        verbose_name="Facilități",
        help_text="Selectează facilitățile disponibile la acest lac"
    )
    price_per_day = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Preț pe zi (RON)",
        help_text="Prețul pentru o zi de pescuit în lei românești (ex: 50.00)"
    )
    rules = models.TextField(
        blank=True,
        verbose_name="Reguli de pescuit",
        help_text="Regulile și restricțiile pentru pescuitul pe acest lac (ex: Permis obligatoriu, Se permite pescuitul din barcă, Program: 06:00-22:00)"
    )
    image = models.ImageField(
        upload_to='lakes/',
        null=True,
        blank=True,
        verbose_name="Imagine",
        help_text="Imaginea principală a lacului (format recomandat: JPG, PNG, max 2MB)"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Activ",
        help_text="Bifează pentru a afișa lacul pe site. Debifează pentru a-l ascunde temporar"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data creării")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Data actualizării")

    class Meta:
        verbose_name = "Lac de pescuit"
        verbose_name_plural = "Lacuri de pescuit"
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            # Generate slug from name, handling Romanian characters
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Lake.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('main:lake_detail', kwargs={'slug': self.slug})

    def get_safe_google_maps_embed(self):
        """Return sanitized Google Maps embed code or None if invalid"""
        if not self.google_maps_embed:
            return None

        # Basic sanitization - only allow iframe tags with Google Maps domains
        embed_code = self.google_maps_embed.strip()

        # Check if it contains iframe and Google Maps domain
        if ('<iframe' in embed_code.lower() and
            ('maps.google.com' in embed_code or 'google.com/maps' in embed_code)):

            # Remove any script tags or other potentially dangerous elements
            embed_code = re.sub(r'<script[^>]*>.*?</script>', '', embed_code, flags=re.IGNORECASE | re.DOTALL)
            embed_code = re.sub(r'<link[^>]*>', '', embed_code, flags=re.IGNORECASE)
            embed_code = re.sub(r'on\w+\s*=\s*["\'][^"\']*["\']', '', embed_code, flags=re.IGNORECASE)

            return mark_safe(embed_code)

        return None

    @property
    def average_rating(self):
        """Calculate average rating from approved reviews"""
        reviews = self.reviews.filter(is_approved=True, is_spam=False)
        if reviews.exists():
            return round(reviews.aggregate(avg_rating=Avg('rating'))['avg_rating'], 2)
        return 0

    @property
    def total_reviews(self):
        """Count approved reviews"""
        return self.reviews.filter(is_approved=True, is_spam=False).count()

    @property
    def rating_distribution(self):
        """Return rating distribution for approved reviews"""
        reviews = self.reviews.filter(is_approved=True, is_spam=False)
        distribution = {i: 0 for i in range(1, 6)}
        for review in reviews:
            distribution[review.rating] += 1
        return distribution

class Video(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name="Titlul videoclipului",
        help_text="Titlul descriptiv al videoclipului (ex: Pescuit la crap pe lacul X)"
    )
    description = models.TextField(
        blank=True,
        verbose_name="Descriere",
        help_text="Descrierea detaliată a videoclipului și conținutului acestuia"
    )
    url = models.URLField(
        verbose_name="Link video",
        help_text="URL-ul complet către videoclip (YouTube, Vimeo, etc.) - ex: https://youtube.com/watch?v=..."
    )
    thumbnail = models.ImageField(
        upload_to='videos/thumbnails/',
        blank=True,
        null=True,
        verbose_name="Imagine de previzualizare",
        help_text="Imaginea care apare înainte de redarea videoclipului (opțional, se poate genera automat)"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Activ",
        help_text="Bifează pentru a afișa videoclipul pe site"
    )
    is_featured = models.BooleanField(
        default=False,
        verbose_name="Video recomandat",
        help_text="Bifează pentru a afișa videoclipul în secțiunea de recomandări"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data creării")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Data actualizării")

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Videoclip'
        verbose_name_plural = 'Videoclipuri'

    def __str__(self):
        return self.title

    @property
    def embed_url(self):
        """Convert video URL to embeddable format"""
        if not self.url:
            return ''

        # Handle YouTube URLs
        if 'youtube.com/watch' in self.url:
            # Extract video ID from URL like https://youtube.com/watch?v=VIDEO_ID
            import re
            match = re.search(r'[?&]v=([^&]+)', self.url)
            if match:
                video_id = match.group(1)
                return f'https://www.youtube.com/embed/{video_id}'
        elif 'youtu.be/' in self.url:
            # Handle short YouTube URLs like https://youtu.be/VIDEO_ID
            video_id = self.url.split('youtu.be/')[-1].split('?')[0]
            return f'https://www.youtube.com/embed/{video_id}'
        elif 'vimeo.com/' in self.url:
            # Handle Vimeo URLs
            video_id = self.url.split('vimeo.com/')[-1].split('?')[0]
            return f'https://player.vimeo.com/video/{video_id}'

        # Return original URL if no conversion needed
        return self.url

class HeroSection(models.Model):
    main_button_text = models.CharField(
        max_length=100,
        default='Alătură-te grupului',
        verbose_name="Textul butonului principal",
        help_text="Textul care apare pe butonul principal din secțiunea hero (ex: Alătură-te grupului)"
    )
    main_button_url = models.URLField(
        default='https://www.facebook.com/rasfatulpescarului',
        verbose_name="Link buton principal",
        help_text="URL-ul către care duce butonul principal (ex: pagina de Facebook)"
    )
    facebook_url = models.URLField(
        default='https://www.facebook.com/rasfatulpescarului',
        verbose_name="Link Facebook",
        help_text="URL-ul complet către pagina de Facebook"
    )
    tiktok_url = models.URLField(
        default='https://www.tiktok.com/@rasfatulpescarului',
        verbose_name="Link TikTok",
        help_text="URL-ul complet către contul de TikTok"
    )
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Data actualizării")

    class Meta:
        verbose_name = 'Secțiune Hero'
        verbose_name_plural = 'Secțiune Hero'

    def __str__(self):
        return 'Hero Section Settings'

    @classmethod
    def get_settings(cls):
        return cls.objects.first()

class OperatingHours(models.Model):
    DAYS_OF_WEEK = [
        ('monday', 'Luni'),
        ('tuesday', 'Marți'),
        ('wednesday', 'Miercuri'),
        ('thursday', 'Joi'),
        ('friday', 'Vineri'),
        ('saturday', 'Sâmbătă'),
        ('sunday', 'Duminică'),
    ]

    lake = models.OneToOneField(
        Lake,
        on_delete=models.CASCADE,
        related_name='operating_hours',
        verbose_name="Lac"
    )

    # Monday
    monday_is_open = models.BooleanField(default=True, verbose_name="Deschis Luni")
    monday_opening_time = models.TimeField(null=True, blank=True, verbose_name="Ora deschidere")
    monday_closing_time = models.TimeField(null=True, blank=True, verbose_name="Ora închidere")
    monday_is_24h = models.BooleanField(default=False, verbose_name="24 ore")
    monday_special_notes = models.CharField(max_length=200, blank=True, verbose_name="Note speciale")

    # Tuesday
    tuesday_is_open = models.BooleanField(default=True, verbose_name="Deschis Marți")
    tuesday_opening_time = models.TimeField(null=True, blank=True, verbose_name="Ora deschidere")
    tuesday_closing_time = models.TimeField(null=True, blank=True, verbose_name="Ora închidere")
    tuesday_is_24h = models.BooleanField(default=False, verbose_name="24 ore")
    tuesday_special_notes = models.CharField(max_length=200, blank=True, verbose_name="Note speciale")

    # Wednesday
    wednesday_is_open = models.BooleanField(default=True, verbose_name="Deschis Miercuri")
    wednesday_opening_time = models.TimeField(null=True, blank=True, verbose_name="Ora deschidere")
    wednesday_closing_time = models.TimeField(null=True, blank=True, verbose_name="Ora închidere")
    wednesday_is_24h = models.BooleanField(default=False, verbose_name="24 ore")
    wednesday_special_notes = models.CharField(max_length=200, blank=True, verbose_name="Note speciale")

    # Thursday
    thursday_is_open = models.BooleanField(default=True, verbose_name="Deschis Joi")
    thursday_opening_time = models.TimeField(null=True, blank=True, verbose_name="Ora deschidere")
    thursday_closing_time = models.TimeField(null=True, blank=True, verbose_name="Ora închidere")
    thursday_is_24h = models.BooleanField(default=False, verbose_name="24 ore")
    thursday_special_notes = models.CharField(max_length=200, blank=True, verbose_name="Note speciale")

    # Friday
    friday_is_open = models.BooleanField(default=True, verbose_name="Deschis Vineri")
    friday_opening_time = models.TimeField(null=True, blank=True, verbose_name="Ora deschidere")
    friday_closing_time = models.TimeField(null=True, blank=True, verbose_name="Ora închidere")
    friday_is_24h = models.BooleanField(default=False, verbose_name="24 ore")
    friday_special_notes = models.CharField(max_length=200, blank=True, verbose_name="Note speciale")

    # Saturday
    saturday_is_open = models.BooleanField(default=True, verbose_name="Deschis Sâmbătă")
    saturday_opening_time = models.TimeField(null=True, blank=True, verbose_name="Ora deschidere")
    saturday_closing_time = models.TimeField(null=True, blank=True, verbose_name="Ora închidere")
    saturday_is_24h = models.BooleanField(default=False, verbose_name="24 ore")
    saturday_special_notes = models.CharField(max_length=200, blank=True, verbose_name="Note speciale")

    # Sunday
    sunday_is_open = models.BooleanField(default=True, verbose_name="Deschis Duminică")
    sunday_opening_time = models.TimeField(null=True, blank=True, verbose_name="Ora deschidere")
    sunday_closing_time = models.TimeField(null=True, blank=True, verbose_name="Ora închidere")
    sunday_is_24h = models.BooleanField(default=False, verbose_name="24 ore")
    sunday_special_notes = models.CharField(max_length=200, blank=True, verbose_name="Note speciale")

    general_notes = models.TextField(
        blank=True,
        verbose_name="Note generale",
        help_text="Informații generale despre program"
    )

    class Meta:
        verbose_name = "Program de funcționare"
        verbose_name_plural = "Programe de funcționare"

    def __str__(self):
        return f"Program {self.lake.name}"

class LakeReview(models.Model):
    RATING_CHOICES = [
        (1, '1 stea'),
        (2, '2 stele'),
        (3, '3 stele'),
        (4, '4 stele'),
        (5, '5 stele'),
    ]

    lake = models.ForeignKey(
        Lake,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name="Lac"
    )
    reviewer_name = models.CharField(
        max_length=100,
        verbose_name="Numele recenzentului",
        help_text="Numele dvs. complet"
    )
    reviewer_email = models.EmailField(
        verbose_name="Email",
        help_text="Pentru verificare (nu va fi afișat public)"
    )
    rating = models.IntegerField(
        choices=RATING_CHOICES,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="Rating"
    )
    title = models.CharField(
        max_length=200,
        verbose_name="Titlul recenziei",
        help_text="Titlu scurt pentru experiența dvs."
    )
    comment = models.TextField(
        max_length=1000,
        validators=[MinLengthValidator(20)],
        verbose_name="Comentariu",
        help_text="Descrieți experiența dvs. la acest lac (minim 20 caractere)"
    )
    visit_date = models.DateField(
        verbose_name="Data vizitei",
        help_text="Când ați vizitat lacul"
    )
    is_approved = models.BooleanField(
        default=False,
        verbose_name="Aprobat"
    )
    is_spam = models.BooleanField(
        default=False,
        verbose_name="Spam"
    )
    ip_address = models.GenericIPAddressField(
        verbose_name="Adresa IP"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data creării")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Data actualizării")

    class Meta:
        verbose_name = "Recenzie lac"
        verbose_name_plural = "Recenzii lacuri"
        ordering = ['-created_at']
        unique_together = ['lake', 'reviewer_email']  # One review per email per lake

    def __str__(self):
        return f"{self.reviewer_name} - {self.lake.name} ({self.rating} stele)"
