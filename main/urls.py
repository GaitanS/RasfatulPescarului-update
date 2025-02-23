from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    # Home
    path('', views.home, name='home'),
    
    # Locations
    path('locations/', views.fishing_locations, name='fishing_locations'),
    path('locations/map/', views.locations_map, name='locations_map'),
    path('api/filter-lakes/', views.filter_lakes, name='filter_lakes'),
    path('api/nearby-lakes/', views.nearby_lakes, name='nearby_lakes'),
    path('locations/county/<slug:county_slug>/', views.county_lakes, name='county_lakes'),
    path('locations/lake/<int:lake_id>/', views.lake_detail, name='lake_detail'),
    
    # Tutorials
    path('tutorials/', views.tutorials, name='tutorials'),
    path('tutorials/<int:video_id>/', views.video_detail, name='video_detail'),
    
    # Pages
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('privacy/', views.privacy, name='privacy'),
    path('api/solunar-data/', views.solunar_data, name='solunar_data'),
    path('solunar-calendar/', views.solunar_calendar, name='solunar_calendar'),
    path('terms/', views.terms, name='terms'),
]
