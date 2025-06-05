from django.db import models
from django.utils.text import slugify

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
    name = models.CharField(
        max_length=200,
        verbose_name="Numele lacului",
        help_text="Numele complet al lacului sau bălții de pescuit"
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
        max_digits=9,
        decimal_places=6,
        verbose_name="Latitudine",
        help_text="Coordonata latitudine (ex: 44.123456). Folosește Google Maps pentru a găsi coordonatele"
    )
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        verbose_name="Longitudine",
        help_text="Coordonata longitudine (ex: 26.123456). Folosește Google Maps pentru a găsi coordonatele"
    )
    fish_types = models.CharField(
        max_length=500,
        verbose_name="Tipuri de pești",
        help_text="Tipurile de pești disponibile, separate prin virgulă (ex: Crap, Șalău, Știucă, Caras)"
    )
    facilities = models.CharField(
        max_length=500,
        verbose_name="Facilități",
        help_text="Facilitățile disponibile, separate prin spații (ex: parcare cazare restaurant toalete)"
    )
    price_per_day = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Preț pe zi (RON)",
        help_text="Prețul pentru o zi de pescuit în lei românești (ex: 50.00)"
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
