from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from django.utils import timezone

# Import models cu try/except pentru a evita erorile
try:
    from .models import Lake, County
except ImportError:
    Lake = None
    County = None

class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'weekly'

    def items(self):
        return ['home', 'about', 'contact', 'solunar_calendar']

    def location(self, item):
        try:
            return reverse(item)
        except:
            return '/'

class LakeSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        if Lake:
            return Lake.objects.filter(is_active=True)[:1000]  # Limitează la 1000
        return []

    def lastmod(self, obj):
        return getattr(obj, 'updated_at', timezone.now())

    def location(self, obj):
        return f'/locations/lake/{obj.slug}/'

class CountySitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.6

    def items(self):
        if County:
            return County.objects.all()
        return []

    def location(self, obj):
        return f'/locations/county/{obj.slug}/'

# Definește sitemaps
sitemaps = {
    'static': StaticViewSitemap,
}

# Adaugă sitemaps pentru modele doar dacă există
if Lake:
    sitemaps['lakes'] = LakeSitemap
if County:
    sitemaps['counties'] = CountySitemap
