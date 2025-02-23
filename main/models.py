from django.db import models
from django.utils.text import slugify

class County(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    region = models.CharField(max_length=50, choices=[
        ('MOLDOVA', 'Moldova'),
        ('MUNTENIA', 'Muntenia'),
        ('OLTENIA', 'Oltenia'),
        ('BANAT', 'Banat'),
        ('CRISANA', 'Crisana'),
        ('MARAMURES', 'Maramures'),
        ('TRANSILVANIA', 'Transilvania'),
        ('DOBROGEA', 'Dobrogea'),
        ('BUCURESTI', 'Bucuresti')
    ])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'counties'
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class SiteSettings(models.Model):
    site_name = models.CharField(max_length=100, default='Răsfățul Pescarului')
    contact_email = models.EmailField(default='contact@rasfatulpescarului.ro')
    phone = models.CharField(max_length=20, default='0700000000')
    address = models.TextField(default='România')
    facebook_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)
    about_text = models.TextField(default='Despre noi')

    class Meta:
        verbose_name = 'Site Settings'
        verbose_name_plural = 'Site Settings'

    def __str__(self):
        return self.site_name

    @classmethod
    def get_settings(cls):
        return cls.objects.first()

class Lake(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    address = models.CharField(max_length=255)
    county = models.ForeignKey(County, on_delete=models.CASCADE, related_name='lakes')
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    fish_types = models.CharField(max_length=500)  # Comma-separated list of fish types
    facilities = models.CharField(max_length=500)  # Comma-separated list of facilities
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='lakes/', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class Video(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    url = models.URLField()
    thumbnail = models.ImageField(upload_to='videos/thumbnails/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Video'
        verbose_name_plural = 'Videos'

    def __str__(self):
        return self.title
