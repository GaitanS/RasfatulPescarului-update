import json
import datetime
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.conf import settings
from django.utils import timezone
from astral import moon, LocationInfo
from astral.sun import sun
from datetime import timedelta
from math import sin, sqrt, atan2, radians, cos
from .models import SiteSettings, County, Video, Lake
from .utils.email import send_contact_confirmation_email, send_contact_admin_email

def calculate_fishing_rating(moon_phase, date):
    base_rating = 5 - abs(moon_phase - 0.5) * 6
    month = date.month
    if 3 <= month <= 8:
        base_rating += 0.5
    elif month in [9, 10]:
        base_rating += 0.25
    return round(max(1, min(5, base_rating)), 2)

def calculate_solunar_data(date):
    location = LocationInfo('Romania', 'Romania', 'Europe/Bucharest', 45.9432, 24.9668)
    moon_phase = moon.phase(date) / 28.0
    s = sun(location.observer, date)
    solar_noon = s['noon']
    solar_midnight = datetime.datetime.combine(date, datetime.time(0, 0)) + timedelta(hours=12)
    
    try:
        moonrise = moon.moonrise(location.observer, date)
        moonset = moon.moonset(location.observer, date)
        
        moonrise_dt = None
        if moonrise:
            moonrise_dt = datetime.datetime.combine(date, moonrise.time())
        
        moonset_dt = None
        if moonset:
            moonset_dt = datetime.datetime.combine(date, moonset.time())

        if moonrise_dt:
            major_start = (moonrise_dt - timedelta(hours=1)).time()
            major_end = (moonrise_dt + timedelta(hours=1)).time()
        else:
            major_start = (solar_noon - timedelta(hours=1)).time()
            major_end = (solar_noon + timedelta(hours=1)).time()
        
        if moonset_dt:
            minor_start = (moonset_dt - timedelta(hours=1)).time()
            minor_end = (moonset_dt + timedelta(hours=1)).time()
        else:
            minor_start = (solar_midnight - timedelta(hours=1)).time()
            minor_end = (solar_midnight + timedelta(hours=1)).time()
    except Exception:
        major_start = (solar_noon - timedelta(hours=1)).time()
        major_end = (solar_noon + timedelta(hours=1)).time()
        minor_start = (solar_midnight - timedelta(hours=1)).time()
        minor_end = (solar_midnight + timedelta(hours=1)).time()
    
    rating = calculate_fishing_rating(moon_phase, date)
    
    return {
        'date': date,
        'moon_phase': moon_phase,
        'major_start': major_start,
        'major_end': major_end,
        'minor_start': minor_start,
        'minor_end': minor_end,
        'rating': rating
    }

def home(request):
    today = timezone.now().date()
    solunar_predictions = []
    
    for i in range(3):
        date = today + timedelta(days=i)
        prediction = calculate_solunar_data(date)
        solunar_predictions.append(prediction)
    
    context = {
        'solunar_predictions': solunar_predictions
    }
    return render(request, 'index/index.html', context)

def fishing_locations(request):
    """View pentru lista de locații de pescuit"""
    lakes = Lake.objects.filter(is_active=True)
    counties = County.objects.prefetch_related('lakes').all()
    return render(request, 'locations/list.html', {
        'lakes': lakes,
        'counties': counties
    })

from django.db.models import Q

@require_http_methods(['GET'])
def filter_lakes(request):
    """API endpoint pentru filtrarea lacurilor"""
    lakes = Lake.objects.filter(is_active=True).select_related('county').prefetch_related('fish_species', 'facilities')

    # Apply county filter
    county_id = request.GET.get('county')
    if county_id:
        lakes = lakes.filter(county_id=county_id)

    # Apply fish types filter
    fish_types = request.GET.getlist('fish_types[]')
    if fish_types:
        lakes = lakes.filter(fish_species__name__in=fish_types).distinct()

    # Apply price filter
    max_price = request.GET.get('max_price')
    if max_price:
        lakes = lakes.filter(price_per_day__lte=max_price)

    # Apply facilities filter
    facilities = request.GET.getlist('facilities[]')
    if facilities:
        lakes = lakes.filter(facilities__name__in=facilities).distinct()

    # Apply rating filter
    min_rating = request.GET.get('min_rating')
    if min_rating:
        try:
            min_rating_value = float(min_rating)
            # Filter lakes that have at least the minimum rating
            # We need to calculate average rating for each lake and filter
            from django.db.models import Avg, Q
            lakes = lakes.annotate(
                avg_rating=Avg('reviews__rating', filter=Q(reviews__is_approved=True, reviews__is_spam=False))
            ).filter(avg_rating__gte=min_rating_value)
        except (ValueError, TypeError):
            pass  # Invalid rating value, ignore filter

    # Format lake data for response
    lakes_data = [{
        'id': lake.id,
        'slug': lake.slug,
        'name': lake.name,
        'address': lake.address,
        'county': lake.county.name,
        'latitude': float(lake.latitude),
        'longitude': float(lake.longitude),
        'fish_species': [{'name': fish.name} for fish in lake.fish_species.all()],
        'facilities': [{'name': facility.name, 'icon_class': facility.icon_class} for facility in lake.facilities.all()],
        'price_per_day': float(lake.price_per_day),
        'image_url': lake.image.url if lake.image else None,
        'average_rating': lake.average_rating,
        'total_reviews': lake.total_reviews
    } for lake in lakes]

    return JsonResponse({'lakes': lakes_data})

@require_http_methods(['GET'])
def debug_lakes(request):
    """Debug endpoint to check lakes data"""
    lakes = Lake.objects.filter(is_active=True).select_related('county').prefetch_related('fish_species', 'facilities')

    lakes_data = [{
        'id': lake.id,
        'slug': lake.slug,
        'name': lake.name,
        'address': lake.address,
        'county': lake.county.name,
        'latitude': float(lake.latitude),
        'longitude': float(lake.longitude),
        'fish_species': [{'name': fish.name} for fish in lake.fish_species.all()],
        'facilities': [{'name': facility.name, 'icon_class': facility.icon_class} for facility in lake.facilities.all()],
        'price_per_day': float(lake.price_per_day),
        'image_url': lake.image.url if lake.image else '/static/images/lake-placeholder.jpg',
        'average_rating': lake.average_rating,
        'total_reviews': lake.total_reviews
    } for lake in lakes]

    return JsonResponse({
        'count': len(lakes_data),
        'lakes': lakes_data
    }, indent=2)

from .models import Lake, County

def locations_map(request):
    """View pentru harta locațiilor"""
    lakes = Lake.objects.filter(is_active=True).select_related('county').prefetch_related('fish_species', 'facilities')
    counties = County.objects.all().order_by('name')

    # Serialize lakes data for JavaScript
    lakes_data = [{
        'id': lake.id,
        'slug': lake.slug,
        'name': lake.name,
        'address': lake.address,
        'county': lake.county.name,
        'latitude': float(lake.latitude),
        'longitude': float(lake.longitude),
        'fish_species': [{'name': fish.name} for fish in lake.fish_species.all()],
        'facilities': [{'name': facility.name, 'icon_class': facility.icon_class} for facility in lake.facilities.all()],
        'price_per_day': float(lake.price_per_day),
        'image_url': lake.image.url if lake.image else '/static/images/lake-placeholder.jpg',
        'average_rating': lake.average_rating,
        'total_reviews': lake.total_reviews
    } for lake in lakes]

    return render(request, 'locations/map.html', {
        'lakes_json': json.dumps(lakes_data),
        'lakes': lakes,
        'counties': counties
    })

def county_lakes(request, county_slug):
    """View pentru lacurile dintr-un județ"""
    county = get_object_or_404(County, slug=county_slug)
    lakes = Lake.objects.filter(county=county, is_active=True)
    return render(request, 'locations/county_lakes.html', {
        'county': county,
        'lakes': lakes
    })

@require_http_methods(['GET'])
def nearby_lakes(request):
    """API endpoint pentru lacurile din apropiere"""
    try:
        user_lat = float(request.GET.get('lat'))
        user_lng = float(request.GET.get('lng'))

        lakes = Lake.objects.filter(is_active=True).select_related('county').prefetch_related('fish_species', 'facilities')

        # Calculate distances and sort by proximity
        lakes_with_distance = []
        for lake in lakes:
            # Calculate distance using Haversine formula
            R = 6371  # Earth's radius in km
            dlat = radians(float(lake.latitude) - user_lat)
            dlon = radians(float(lake.longitude) - user_lng)
            a = sin(dlat/2)**2 + cos(radians(user_lat)) * cos(radians(float(lake.latitude))) * sin(dlon/2)**2
            c = 2 * atan2(sqrt(a), sqrt(1-a))
            distance = R * c

            lakes_with_distance.append({
                'id': lake.id,
                'slug': lake.slug,
                'name': lake.name,
                'address': lake.address,
                'county': lake.county.name,
                'latitude': float(lake.latitude),
                'longitude': float(lake.longitude),
                'fish_species': [{'name': fish.name} for fish in lake.fish_species.all()],
                'facilities': [{'name': facility.name, 'icon_class': facility.icon_class} for facility in lake.facilities.all()],
                'price_per_day': float(lake.price_per_day),
                'image_url': lake.image.url if lake.image else None,
                'distance': round(distance, 1),
                'average_rating': lake.average_rating,
                'total_reviews': lake.total_reviews
            })

        # Sort by distance and limit to 6 nearest lakes
        lakes_with_distance.sort(key=lambda x: x['distance'])
        nearest_lakes = lakes_with_distance[:6]

        return JsonResponse({'lakes': nearest_lakes})
    except (ValueError, TypeError):
        return JsonResponse({'error': 'Invalid coordinates'}, status=400)

def lake_detail(request, slug):
    """View pentru detaliile unui lac"""
    lake = get_object_or_404(Lake.objects.select_related('county'), slug=slug, is_active=True)

    # Get nearby lakes (within same county for now)
    nearby_lakes = Lake.objects.filter(
        county=lake.county,
        is_active=True
    ).exclude(id=lake.id)[:3]

    context = {
        'lake': lake,
        'nearby_lakes': nearby_lakes
    }
    return render(request, 'locations/lake_detail.html', context)

def add_review(request, lake_id):
    """Add a review for a lake"""
    if request.method == 'POST':
        from .models import LakeReview

        lake = get_object_or_404(Lake, id=lake_id, is_active=True)

        # Get client IP
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')

        try:
            review = LakeReview.objects.create(
                lake=lake,
                reviewer_name=request.POST.get('reviewer_name'),
                reviewer_email=request.POST.get('reviewer_email'),
                rating=int(request.POST.get('rating')),
                title=request.POST.get('title'),
                comment=request.POST.get('comment'),
                visit_date=request.POST.get('visit_date'),
                ip_address=ip
            )
            messages.success(request, 'Recenzia dvs. a fost trimisă cu succes! Va fi publicată după aprobare.')
        except Exception as e:
            messages.error(request, 'A apărut o eroare la trimiterea recenziei. Vă rugăm să încercați din nou.')

        return redirect('main:lake_detail', slug=lake.slug)

    return redirect('main:fishing_locations')

def tutorials(request):
    """View pentru lista de tutoriale video"""
    videos = Video.objects.filter(is_active=True).order_by('-created_at')
    
    # Pagination
    paginator = Paginator(videos, 12)
    page = request.GET.get('page')
    try:
        videos = paginator.page(page)
    except PageNotAnInteger:
        videos = paginator.page(1)
    except EmptyPage:
        videos = paginator.page(paginator.num_pages)
    
    return render(request, 'tutorials/list.html', {'videos': videos})

def video_detail(request, video_id):
    """View pentru detaliile unui tutorial video"""
    video = get_object_or_404(Video, id=video_id, is_active=True)
    
    # Get related videos
    related_videos = Video.objects.filter(
        is_active=True
    ).exclude(id=video.id).order_by('?')[:4]
    
    return render(request, 'tutorials/detail.html', {
        'video': video,
        'related_videos': related_videos
    })

def about(request):
    """View pentru pagina Despre noi"""
    return render(request, 'pages/about.html')

def contact(request):
    """View pentru pagina de contact"""
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        # Store form data in case of error
        form_data = {
            'name': name,
            'email': email,
            'subject': subject,
            'message': message
        }
        
        # Basic validation
        if not all([name, email, subject, message]):
            messages.error(
                request,
                'Te rugăm să completezi toate câmpurile obligatorii.'
            )
            return render(request, 'pages/contact.html', {'form_data': form_data})
        
        try:
            # Send contact emails
            send_contact_confirmation_email(email, name)
            send_contact_admin_email(name, email, subject, message)
            
            messages.success(
                request,
                'Mesajul tău a fost trimis cu succes! Te vom contacta în curând.'
            )
            return redirect('main:contact')
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f'Error sending contact form emails: {str(e)}')
            logger.exception('Full traceback:')
            
            messages.error(
                request,
                'A apărut o eroare la trimiterea mesajului. Te rugăm să încerci din nou.'
            )
            return render(request, 'pages/contact.html', {'form_data': form_data})
    
    return render(request, 'pages/contact.html')

@require_http_methods(['GET'])
def solunar_data(request):
    """API endpoint pentru date solunar"""
    today = timezone.now().date()
    predictions = []
    
    for i in range(3):
        date = today + timedelta(days=i)
        prediction = calculate_solunar_data(date)
        # Convert datetime objects to string format for JSON serialization
        predictions.append({
            'date': date.strftime('%Y-%m-%d'),
            'moon_phase': prediction['moon_phase'],
            'major_start': prediction['major_start'].strftime('%H:%M'),
            'major_end': prediction['major_end'].strftime('%H:%M'),
            'minor_start': prediction['minor_start'].strftime('%H:%M'),
            'minor_end': prediction['minor_end'].strftime('%H:%M'),
            'rating': prediction['rating']
        })
    
    return JsonResponse({'predictions': predictions})

def solunar_calendar(request):
    """View pentru calendarul solunar lunar"""
    from dateutil.relativedelta import relativedelta
    import calendar
    
    # Get year and month from query params or use current date
    year = int(request.GET.get('year', timezone.now().year))
    month = int(request.GET.get('month', timezone.now().month))
    
    # Get all days in the selected month
    first_day = datetime.date(year, month, 1)
    last_day = first_day + relativedelta(months=1, days=-1)
    
    # Calculate solunar data for each day
    calendar_data = []
    current_date = first_day
    while current_date <= last_day:
        prediction = calculate_solunar_data(current_date)
        calendar_data.append(prediction)
        current_date += timedelta(days=1)
    
    # Romanian month names
    months = [
        'Ianuarie', 'Februarie', 'Martie', 'Aprilie', 'Mai', 'Iunie',
        'Iulie', 'August', 'Septembrie', 'Octombrie', 'Noiembrie', 'Decembrie'
    ]
    
    context = {
        'calendar_data': calendar_data,
        'current_year': year,
        'current_month': month,
        'years_range': range(timezone.now().year - 2, timezone.now().year + 3),
        'months': [(i+1, name) for i, name in enumerate(months)]
    }
    return render(request, 'solunar/calendar.html', context)

def terms(request):
    """View pentru pagina de termeni și condiții"""
    return render(request, 'pages/terms.html')

def privacy(request):
    """View function for the privacy policy page."""
    return render(request, 'pages/privacy.html')
