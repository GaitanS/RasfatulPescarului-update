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
    
    # Account
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('verify-email/<str:uidb64>/<str:token>/', views.verify_email, name='verify_email'),
    path('password-reset/', views.password_reset, name='password_reset'),
    path('password-reset/<str:uidb64>/<str:token>/', views.password_reset_confirm, name='password_reset_confirm'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/change-password/', views.change_password, name='change_password'),
    
    # Orders
    path('orders/', views.orders, name='orders'),
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),
    path('orders/<int:order_id>/cancel/', views.order_cancel, name='order_cancel'),
    
    # Pages
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('privacy/', views.privacy, name='privacy'),
    path('api/solunar-data/', views.solunar_data, name='solunar_data'),
    path('solunar-calendar/', views.solunar_calendar, name='solunar_calendar'),
    path('terms/', views.terms, name='terms'),
]
