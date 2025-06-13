from django.urls import path
from . import views, auth_views

app_name = 'main'

urlpatterns = [
    # Home
    path('', views.home, name='home'),

    # Authentication URLs (Romanian)
    path('înregistrare/', auth_views.register_view, name='inregistrare'),
    path('autentificare/', auth_views.login_view, name='autentificare'),
    path('deconectare/', auth_views.logout_view, name='deconectare'),
    path('recuperare-parola/', auth_views.password_reset_view, name='recuperare_parola'),
    path('recuperare-parola/trimis/', auth_views.password_reset_done_view, name='password_reset_done'),
    path('resetare-parola/<uidb64>/<token>/', auth_views.password_reset_confirm_view, name='password_reset_confirm'),
    path('resetare-parola/complet/', auth_views.password_reset_complete_view, name='password_reset_complete'),

    # User profile URLs (Romanian)
    path('utilizator/profil/', auth_views.profile_view, name='utilizator_profil'),
    path('utilizator/editare-profil/', auth_views.edit_profile_view, name='editare_profil'),
    path('utilizator/schimbare-parola/', auth_views.change_password_view, name='schimbare_parola'),
    path('utilizator/balțile-mele/', auth_views.my_lakes_view, name='baltile_mele'),

    # Lake management URLs (Romanian)
    path('baltă/creează/', auth_views.create_lake_view, name='creaza_balta'),
    path('baltă/<slug:slug>/editează/', auth_views.edit_lake_view, name='editeaza_balta'),
    path('baltă/<slug:slug>/șterge/', auth_views.delete_lake_view, name='sterge_balta'),
    path('baltă/<slug:slug>/fotografii/', auth_views.manage_lake_photos_view, name='manage_lake_photos'),
    path('baltă/<slug:slug>/fotografii/<int:photo_id>/șterge/', auth_views.delete_lake_photo_view, name='delete_lake_photo'),
    path('baltă/<slug:slug>/fotografii/<int:photo_id>/principală/', auth_views.set_main_photo_view, name='set_main_photo'),

    # Lake detail URL (Romanian)
    path('baltă/<slug:slug>/', views.lake_detail, name='balta_detail'),

    # Legacy locations URLs (keep for backward compatibility)
    path('locations/', views.fishing_locations, name='fishing_locations'),
    path('locations/map/', views.locations_map, name='locations_map'),
    path('locations/county/<slug:county_slug>/', views.county_lakes, name='county_lakes'),
    path('locations/lake/<slug:slug>/', views.lake_detail, name='lake_detail'),
    path('locations/lake/<int:lake_id>/add-review/', views.add_review, name='add_review'),

    # API endpoints
    path('api/filter-lakes/', views.filter_lakes, name='filter_lakes'),
    path('api/nearby-lakes/', views.nearby_lakes, name='nearby_lakes'),
    path('api/debug-lakes/', views.debug_lakes, name='debug_lakes'),

    # REST API endpoints (Romanian)
    path('utilizator/me/', auth_views.api_user_profile, name='api_user_profile'),
    path('baltă/api/', auth_views.api_user_lakes, name='api_user_lakes'),
    
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

    # Test iframe
    path('test-iframe/', views.test_iframe, name='test_iframe'),
]
