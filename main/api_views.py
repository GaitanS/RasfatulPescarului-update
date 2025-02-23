from rest_framework import viewsets
from rest_framework.response import Response
from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie

# Empty api_views.py file - removed all shop-related viewsets and serializers
# This file can be used later to add new API endpoints as needed