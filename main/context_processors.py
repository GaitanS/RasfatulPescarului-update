from django.conf import settings
from .models import SiteSettings

def cart_processor(request):
    """Empty context processor since cart functionality has been removed"""
    return {
        'debug': settings.DEBUG
    }

from .models import HeroSection

from .models import HeroSection, FooterSettings

def site_settings(request):
    """Make site settings, HeroSection, and FooterSettings available to all templates"""
    try:
        settings_obj = SiteSettings.objects.first()
        hero_obj = HeroSection.objects.first()
        footer_obj = FooterSettings.objects.first()
        return {'site_settings': settings_obj, 'hero': hero_obj, 'footer': footer_obj}
    except:
        return {'site_settings': None, 'hero': None, 'footer': None}
