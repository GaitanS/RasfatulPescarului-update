from django.conf import settings
from .models import SiteSettings

def cart_processor(request):
    """Empty context processor since cart functionality has been removed"""
    return {
        'debug': settings.DEBUG
    }

def site_settings(request):
    """Make site settings available to all templates"""
    try:
        settings_obj = SiteSettings.objects.first()
        return {'site_settings': settings_obj}
    except:
        return {'site_settings': None}
