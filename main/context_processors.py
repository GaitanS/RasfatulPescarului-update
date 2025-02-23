from django.conf import settings

def cart_processor(request):
    """Empty context processor since cart functionality has been removed"""
    return {
        'debug': settings.DEBUG
    }
