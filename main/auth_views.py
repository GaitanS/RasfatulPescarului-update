from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse, Http404
from django.views.decorators.http import require_http_methods
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from .forms import CustomUserCreationForm, CustomAuthenticationForm, UserProfileForm, LakeForm, LakePhotoForm
from .models import Lake, UserProfile, LakePhoto
import json


def register_view(request):
    """User registration view"""
    if request.user.is_authenticated:
        return redirect('main:utilizator_profil')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Contul pentru {username} a fost creat cu succes! Vă puteți autentifica acum.')
            return redirect('main:autentificare')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'auth/register.html', {'form': form})


def login_view(request):
    """User login view"""
    if request.user.is_authenticated:
        return redirect('main:utilizator_profil')
    
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Bine ați venit, {user.get_full_name() or user.username}!')
                next_url = request.GET.get('next')
                if next_url:
                    return redirect(next_url)
                return redirect('main:utilizator_profil')
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'auth/login.html', {'form': form})


def logout_view(request):
    """User logout view"""
    logout(request)
    messages.success(request, 'V-ați deconectat cu succes!')
    return redirect('main:home')


@login_required
def profile_view(request):
    """User profile view"""
    try:
        profile = request.user.profile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=request.user)
    
    # Get user's lakes
    user_lakes = Lake.objects.filter(owner=request.user, is_active=True).order_by('-updated_at')
    
    # Pagination for lakes
    paginator = Paginator(user_lakes, 6)  # Show 6 lakes per page
    page_number = request.GET.get('page')
    lakes_page = paginator.get_page(page_number)
    
    context = {
        'profile': profile,
        'lakes_page': lakes_page,
        'total_lakes': user_lakes.count()
    }
    return render(request, 'auth/profile.html', context)


@login_required
def edit_profile_view(request):
    """Edit user profile view"""
    try:
        profile = request.user.profile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=request.user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profilul dvs. a fost actualizat cu succes!')
            return redirect('main:utilizator_profil')
    else:
        form = UserProfileForm(instance=profile, user=request.user)
    
    return render(request, 'auth/edit_profile.html', {'form': form})


@login_required
def change_password_view(request):
    """Change password view"""
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Parola dvs. a fost schimbată cu succes!')
            return redirect('main:utilizator_profil')
    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, 'auth/change_password.html', {'form': form})


@login_required
def create_lake_view(request):
    """Create new lake view"""
    if request.method == 'POST':
        form = LakeForm(request.POST, request.FILES)
        if form.is_valid():
            lake = form.save(commit=False)
            lake.owner = request.user
            lake.save()
            form.save_m2m()  # Save many-to-many relationships

            # Process uploaded photos
            photo_count = 0
            for key, file in request.FILES.items():
                if key.startswith('photo_') and photo_count < 10:
                    # Create LakePhoto instance
                    photo = LakePhoto(
                        lake=lake,
                        image=file,
                        title=f"Fotografie {photo_count + 1}",
                        is_main=(photo_count == 0)  # First photo is main
                    )
                    photo.save()
                    photo_count += 1

            if photo_count > 0:
                messages.success(request, f'Balta "{lake.name}" a fost creată cu succes cu {photo_count} fotografii!')
            else:
                messages.success(request, f'Balta "{lake.name}" a fost creată cu succes!')
            return redirect('main:balta_detail', slug=lake.slug)
    else:
        form = LakeForm()

    return render(request, 'lakes/create_lake.html', {'form': form})


@login_required
def edit_lake_view(request, slug):
    """Edit lake view"""
    lake = get_object_or_404(Lake, slug=slug)
    
    # Check if user can edit this lake
    if not lake.can_edit(request.user):
        messages.error(request, 'Nu aveți permisiunea să editați această baltă.')
        return redirect('main:balta_detail', slug=lake.slug)
    
    if request.method == 'POST':
        form = LakeForm(request.POST, instance=lake)
        if form.is_valid():
            form.save()
            messages.success(request, f'Balta "{lake.name}" a fost actualizată cu succes!')
            return redirect('main:balta_detail', slug=lake.slug)
    else:
        form = LakeForm(instance=lake)
    
    return render(request, 'lakes/edit_lake.html', {'form': form, 'lake': lake})


@login_required
def delete_lake_view(request, slug):
    """Delete lake view"""
    lake = get_object_or_404(Lake, slug=slug)
    
    # Check if user can delete this lake
    if not lake.can_edit(request.user):
        messages.error(request, 'Nu aveți permisiunea să ștergeți această baltă.')
        return redirect('main:balta_detail', slug=lake.slug)
    
    if request.method == 'POST':
        lake_name = lake.name
        lake.delete()
        messages.success(request, f'Balta "{lake_name}" a fost ștearsă cu succes!')
        return redirect('main:utilizator_profil')
    
    return render(request, 'lakes/delete_lake.html', {'lake': lake})


@login_required
def manage_lake_photos_view(request, slug):
    """Manage lake photos view"""
    lake = get_object_or_404(Lake, slug=slug)
    
    # Check if user can edit this lake
    if not lake.can_edit(request.user):
        messages.error(request, 'Nu aveți permisiunea să gestionați fotografiile acestei balți.')
        return redirect('main:balta_detail', slug=lake.slug)
    
    photos = lake.photos.all().order_by('order', 'created_at')
    
    if request.method == 'POST':
        form = LakePhotoForm(request.POST, request.FILES)
        if form.is_valid():
            # Check if lake already has 10 photos
            if photos.count() >= 10:
                messages.error(request, 'O baltă poate avea maximum 10 fotografii.')
            else:
                photo = form.save(commit=False)
                photo.lake = lake
                photo.save()
                messages.success(request, 'Fotografia a fost adăugată cu succes!')
                return redirect('main:manage_lake_photos', slug=lake.slug)
    else:
        form = LakePhotoForm()
    
    context = {
        'lake': lake,
        'photos': photos,
        'form': form,
        'can_add_more': photos.count() < 10
    }
    return render(request, 'lakes/manage_photos.html', context)


@login_required
@require_http_methods(["POST"])
def delete_lake_photo_view(request, slug, photo_id):
    """Delete lake photo via AJAX"""
    lake = get_object_or_404(Lake, slug=slug)
    
    # Check if user can edit this lake
    if not lake.can_edit(request.user):
        return JsonResponse({'success': False, 'error': 'Nu aveți permisiunea să ștergeți această fotografie.'})
    
    try:
        photo = get_object_or_404(LakePhoto, id=photo_id, lake=lake)
        photo.delete()
        return JsonResponse({'success': True, 'message': 'Fotografia a fost ștearsă cu succes!'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': 'A apărut o eroare la ștergerea fotografiei.'})


@login_required
@require_http_methods(["POST"])
def set_main_photo_view(request, slug, photo_id):
    """Set main photo for lake via AJAX"""
    lake = get_object_or_404(Lake, slug=slug)
    
    # Check if user can edit this lake
    if not lake.can_edit(request.user):
        return JsonResponse({'success': False, 'error': 'Nu aveți permisiunea să modificați această baltă.'})
    
    try:
        # Unset all main photos for this lake
        LakePhoto.objects.filter(lake=lake, is_main=True).update(is_main=False)
        
        # Set the selected photo as main
        photo = get_object_or_404(LakePhoto, id=photo_id, lake=lake)
        photo.is_main = True
        photo.save()
        
        return JsonResponse({'success': True, 'message': 'Fotografia principală a fost setată cu succes!'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': 'A apărut o eroare la setarea fotografiei principale.'})


@login_required
def my_lakes_view(request):
    """View for listing user's lakes"""
    lakes = Lake.objects.filter(owner=request.user).order_by('-updated_at').prefetch_related('photos', 'reviews')

    # Calculate statistics
    total_lakes = lakes.count()
    active_lakes = lakes.filter(is_active=True).count()
    total_photos = sum(lake.photos.count() for lake in lakes)
    total_reviews = sum(lake.reviews.count() for lake in lakes)

    context = {
        'lakes': lakes,
        'total_lakes': total_lakes,
        'active_lakes': active_lakes,
        'total_photos': total_photos,
        'total_reviews': total_reviews,
    }
    return render(request, 'lakes/my_lakes.html', context)


# API endpoints for REST functionality
@login_required
@require_http_methods(["GET"])
def api_user_profile(request):
    """API endpoint to get user profile data"""
    try:
        profile = request.user.profile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=request.user)
    
    data = {
        'username': request.user.username,
        'email': request.user.email,
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
        'phone': profile.phone,
        'city': profile.city,
        'county': profile.county.name if profile.county else None,
        'bio': profile.bio,
        'avatar_url': profile.avatar.url if profile.avatar else None,
        'created_at': profile.created_at.isoformat(),
        'updated_at': profile.updated_at.isoformat()
    }
    
    return JsonResponse(data)


@login_required
@require_http_methods(["GET"])
def api_user_lakes(request):
    """API endpoint to get user's lakes"""
    lakes = Lake.objects.filter(owner=request.user, is_active=True).order_by('-updated_at')
    
    data = []
    for lake in lakes:
        data.append({
            'id': lake.id,
            'name': lake.name,
            'slug': lake.slug,
            'address': lake.address,
            'county': lake.county.name,
            'price_per_day': str(lake.price_per_day),
            'created_at': lake.created_at.isoformat(),
            'updated_at': lake.updated_at.isoformat(),
            'url': lake.get_absolute_url(),
            'main_photo_url': lake.get_main_photo().url if lake.get_main_photo() else None
        })
    
    return JsonResponse({'lakes': data, 'total': len(data)})
