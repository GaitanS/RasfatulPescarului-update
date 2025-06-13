from django.contrib import admin
from django.contrib.admin.widgets import AdminTimeWidget
from django import forms
from django.db import models
from .models import (
    SiteSettings, County, Lake, Video, HeroSection, FooterSettings,
    FishSpecies, Facility, OperatingHours, LakeReview, LakePhoto, UserProfile, ContactMessage, ContactSettings
)

class OperatingHoursForm(forms.ModelForm):
    """Custom form for OperatingHours with time picker widgets"""

    class Meta:
        model = OperatingHours
        fields = '__all__'
        widgets = {
            # Monday
            'monday_opening_time': AdminTimeWidget(format='%H:%M'),
            'monday_closing_time': AdminTimeWidget(format='%H:%M'),
            # Tuesday
            'tuesday_opening_time': AdminTimeWidget(format='%H:%M'),
            'tuesday_closing_time': AdminTimeWidget(format='%H:%M'),
            # Wednesday
            'wednesday_opening_time': AdminTimeWidget(format='%H:%M'),
            'wednesday_closing_time': AdminTimeWidget(format='%H:%M'),
            # Thursday
            'thursday_opening_time': AdminTimeWidget(format='%H:%M'),
            'thursday_closing_time': AdminTimeWidget(format='%H:%M'),
            # Friday
            'friday_opening_time': AdminTimeWidget(format='%H:%M'),
            'friday_closing_time': AdminTimeWidget(format='%H:%M'),
            # Saturday
            'saturday_opening_time': AdminTimeWidget(format='%H:%M'),
            'saturday_closing_time': AdminTimeWidget(format='%H:%M'),
            # Sunday
            'sunday_opening_time': AdminTimeWidget(format='%H:%M'),
            'sunday_closing_time': AdminTimeWidget(format='%H:%M'),
        }

class CustomFacilityForm(forms.ModelForm):
    """Custom form for Lake with grouped facility selection"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Group facilities by Romanian category for better display
        if 'facilities' in self.fields:
            from .models import Facility
            facilities = Facility.objects.filter(is_active=True).order_by('category', 'name')

            # Create grouped choices
            grouped_choices = []
            current_category = None
            current_group = []

            for facility in facilities:
                category_ro = facility.get_category_display_romanian()
                if current_category != category_ro:
                    if current_group:
                        grouped_choices.append((current_category, current_group))
                    current_category = category_ro
                    current_group = []
                current_group.append((facility.pk, facility.name))

            # Add the last group
            if current_group:
                grouped_choices.append((current_category, current_group))

            # Update the field choices
            self.fields['facilities'].choices = grouped_choices

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Informații generale', {
            'fields': ('site_name', 'contact_email', 'phone', 'address')
        }),
        ('Rețele sociale', {
            'fields': ('facebook_url', 'instagram_url', 'youtube_url'),
            'description': 'Link-urile către paginile de social media'
        }),
        ('Conținut', {
            'fields': ('about_text',)
        }),
    )

    def has_add_permission(self, request):
        # Only allow one instance of SiteSettings
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        # Prevent deletion of the only instance
        return False

@admin.register(FooterSettings)
class FooterSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Informații de contact', {
            'fields': ('contact_info', 'address', 'phone', 'email'),
            'description': 'Informațiile care apar în footer-ul site-ului'
        }),
        ('Program', {
            'fields': ('working_hours',)
        }),
    )

    def has_add_permission(self, request):
        # Only allow one instance of FooterSettings
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        # Prevent deletion of the only instance
        return False

@admin.register(County)
class CountyAdmin(admin.ModelAdmin):
    list_display = ['name', 'region', 'get_lakes_count', 'created_at']
    list_filter = ['region']
    search_fields = ['name', 'region']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Informații județ', {
            'fields': ('name', 'slug', 'region')
        }),
        ('Informații sistem', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def get_lakes_count(self, obj):
        return obj.lakes.count()
    get_lakes_count.short_description = 'Numărul de lacuri'

@admin.register(FishSpecies)
class FishSpeciesAdmin(admin.ModelAdmin):
    list_display = ['name', 'scientific_name', 'category', 'is_active', 'created_at']
    list_filter = ['category', 'is_active', 'created_at']
    search_fields = ['name', 'scientific_name']
    readonly_fields = ['created_at', 'updated_at']
    list_editable = ['is_active']

    fieldsets = (
        ('Informații specie', {
            'fields': ('name', 'scientific_name', 'category')
        }),
        ('Setări', {
            'fields': ('is_active',)
        }),
        ('Informații sistem', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Facility)
class FacilityAdmin(admin.ModelAdmin):
    list_display = ['name', 'get_category_display_romanian', 'icon_class', 'is_active', 'created_at']
    list_filter = ['category', 'is_active', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at']
    list_editable = ['is_active']

    def get_category_display_romanian(self, obj):
        return obj.get_category_display_romanian()
    get_category_display_romanian.short_description = 'Categoria'

    fieldsets = (
        ('Informații facilitate', {
            'fields': ('name', 'icon_class', 'category', 'description')
        }),
        ('Setări', {
            'fields': ('is_active',)
        }),
        ('Informații sistem', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'get_full_name', 'phone', 'city', 'county', 'created_at']
    list_filter = ['county', 'created_at']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'user__email', 'phone', 'city']
    readonly_fields = ['created_at', 'updated_at']

    def get_full_name(self, obj):
        return obj.get_full_name()
    get_full_name.short_description = 'Nume complet'

    fieldsets = (
        ('Utilizator', {
            'fields': ('user',)
        }),
        ('Informații personale', {
            'fields': ('phone', 'city', 'county', 'bio')
        }),
        ('Avatar', {
            'fields': ('avatar',)
        }),
        ('Informații sistem', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

class OperatingHoursInline(admin.StackedInline):
    model = OperatingHours
    form = OperatingHoursForm
    extra = 0
    max_num = 1

    fieldsets = (
        ('Luni', {
            'fields': ('monday_is_open', 'monday_opening_time', 'monday_closing_time', 'monday_is_24h', 'monday_special_notes'),
            'classes': ('collapse',)
        }),
        ('Marți', {
            'fields': ('tuesday_is_open', 'tuesday_opening_time', 'tuesday_closing_time', 'tuesday_is_24h', 'tuesday_special_notes'),
            'classes': ('collapse',)
        }),
        ('Miercuri', {
            'fields': ('wednesday_is_open', 'wednesday_opening_time', 'wednesday_closing_time', 'wednesday_is_24h', 'wednesday_special_notes'),
            'classes': ('collapse',)
        }),
        ('Joi', {
            'fields': ('thursday_is_open', 'thursday_opening_time', 'thursday_closing_time', 'thursday_is_24h', 'thursday_special_notes'),
            'classes': ('collapse',)
        }),
        ('Vineri', {
            'fields': ('friday_is_open', 'friday_opening_time', 'friday_closing_time', 'friday_is_24h', 'friday_special_notes'),
            'classes': ('collapse',)
        }),
        ('Sâmbătă', {
            'fields': ('saturday_is_open', 'saturday_opening_time', 'saturday_closing_time', 'saturday_is_24h', 'saturday_special_notes'),
            'classes': ('collapse',)
        }),
        ('Duminică', {
            'fields': ('sunday_is_open', 'sunday_opening_time', 'sunday_closing_time', 'sunday_is_24h', 'sunday_special_notes'),
            'classes': ('collapse',)
        }),
        ('Note generale', {
            'fields': ('general_notes',)
        }),
    )

class LakePhotoInline(admin.TabularInline):
    """Inline admin for managing lake photos"""
    model = LakePhoto
    extra = 1
    max_num = 10
    fields = ['image', 'is_main']
    readonly_fields = ['created_at', 'updated_at']
    verbose_name = "Fotografie"
    verbose_name_plural = "Fotografii galerie (max 10)"

    def get_extra(self, request, obj=None, **kwargs):
        """Reduce extra forms if lake already has photos"""
        if obj and obj.photos.exists():
            return 0
        return 1

@admin.register(Lake)
class LakeAdmin(admin.ModelAdmin):
    form = CustomFacilityForm
    list_display = ['name', 'owner', 'county', 'lake_type', 'price_per_day', 'is_active', 'created_at']
    list_filter = ['county', 'lake_type', 'is_active', 'created_at', 'owner']
    search_fields = ['name', 'description', 'address', 'rules', 'owner__username', 'owner__first_name', 'owner__last_name']
    readonly_fields = ['created_at', 'updated_at']
    list_editable = ['is_active']
    list_per_page = 20
    filter_horizontal = ['fish_species', 'facilities']
    inlines = [OperatingHoursInline, LakePhotoInline]

    fieldsets = (
        ('Proprietar', {
            'fields': ('owner',)
        }),
        ('Informații de bază', {
            'fields': ('name', 'slug', 'county', 'address', 'description')
        }),
        ('Localizare', {
            'fields': ('latitude', 'longitude', 'google_maps_embed'),
            'description': 'Coordonatele GPS ale lacului sau cod embed Google Maps. Poți găsi coordonatele pe Google Maps făcând click dreapta pe locație.'
        }),
        ('Detalii pescuit', {
            'fields': ('lake_type', 'fish_species', 'facilities', 'price_per_day', 'rules')
        }),
        ('Date de contact', {
            'fields': ('contact_phone', 'contact_email')
        }),
        ('Informații suplimentare', {
            'fields': ('number_of_stands', 'surface_area', 'depth_min', 'depth_max', 'depth_average',
                      'length_min', 'length_max', 'width_min', 'width_max'),
            'classes': ('collapse',)
        }),
        ('Rețele sociale și web', {
            'fields': ('website', 'facebook_url', 'instagram_url'),
            'classes': ('collapse',)
        }),
        ('Media și vizibilitate', {
            'fields': ('image', 'is_active'),
            'description': 'Imaginea principală (pentru compatibilitate) și galeria de fotografii (se gestionează mai jos în secțiunea "Fotografii galerie")'
        }),
        ('Informații sistem', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active', 'is_featured', 'created_at']
    list_filter = ['is_active', 'is_featured', 'created_at']
    search_fields = ['title', 'description']
    readonly_fields = ['created_at', 'updated_at']
    list_editable = ['is_active', 'is_featured']

    fieldsets = (
        ('Informații video', {
            'fields': ('title', 'description', 'url')
        }),
        ('Setări afișare', {
            'fields': ('thumbnail', 'is_active', 'is_featured')
        }),
        ('Informații sistem', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(HeroSection)
class HeroSectionAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Buton principal', {
            'fields': ('main_button_text', 'main_button_url'),
            'description': 'Setările pentru butonul principal din secțiunea hero'
        }),
        ('Link-uri sociale', {
            'fields': ('facebook_url', 'tiktok_url')
        }),
        ('Informații sistem', {
            'fields': ('updated_at',),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ['updated_at']

    def has_add_permission(self, request):
        # Only allow one instance of HeroSection
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        # Prevent deletion of the only instance
        return False

@admin.register(LakeReview)
class LakeReviewAdmin(admin.ModelAdmin):
    list_display = ['reviewer_name', 'lake', 'rating', 'title', 'visit_date', 'is_approved', 'is_spam', 'created_at']
    list_filter = ['rating', 'is_approved', 'is_spam', 'visit_date', 'created_at', 'lake__county']
    search_fields = ['reviewer_name', 'reviewer_email', 'title', 'comment', 'lake__name']
    readonly_fields = ['created_at', 'updated_at', 'ip_address']
    list_editable = ['is_approved', 'is_spam']
    list_per_page = 25
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Informații recenzie', {
            'fields': ('lake', 'reviewer_name', 'reviewer_email', 'rating', 'title', 'comment', 'visit_date')
        }),
        ('Moderare', {
            'fields': ('is_approved', 'is_spam')
        }),
        ('Informații sistem', {
            'fields': ('ip_address', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    actions = ['approve_reviews', 'mark_as_spam', 'mark_as_not_spam']

    def approve_reviews(self, request, queryset):
        updated = queryset.update(is_approved=True, is_spam=False)
        self.message_user(request, f'{updated} recenzii au fost aprobate.')
    approve_reviews.short_description = 'Aprobă recenziile selectate'

    def mark_as_spam(self, request, queryset):
        updated = queryset.update(is_spam=True, is_approved=False)
        self.message_user(request, f'{updated} recenzii au fost marcate ca spam.')
    mark_as_spam.short_description = 'Marchează ca spam'

    def mark_as_not_spam(self, request, queryset):
        updated = queryset.update(is_spam=False)
        self.message_user(request, f'{updated} recenzii au fost demarcate ca spam.')
    mark_as_not_spam.short_description = 'Demarchează ca spam'


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'get_short_message', 'created_at', 'is_read', 'is_replied']
    list_filter = ['is_read', 'is_replied', 'created_at']
    search_fields = ['name', 'email', 'subject', 'message']
    readonly_fields = ['name', 'email', 'subject', 'message', 'ip_address', 'created_at']
    list_per_page = 25
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Informații mesaj', {
            'fields': ('name', 'email', 'subject', 'message', 'ip_address', 'created_at')
        }),
        ('Status', {
            'fields': ('is_read', 'is_replied')
        }),
        ('Note administrative', {
            'fields': ('admin_notes',),
            'classes': ('collapse',)
        }),
    )

    actions = ['mark_as_read', 'mark_as_replied', 'mark_as_unread']

    def mark_as_read(self, request, queryset):
        updated = queryset.update(is_read=True)
        self.message_user(request, f'{updated} mesaje au fost marcate ca citite.')
    mark_as_read.short_description = 'Marchează ca citite'

    def mark_as_replied(self, request, queryset):
        updated = queryset.update(is_replied=True, is_read=True)
        self.message_user(request, f'{updated} mesaje au fost marcate ca având răspuns.')
    mark_as_replied.short_description = 'Marchează ca având răspuns'

    def mark_as_unread(self, request, queryset):
        updated = queryset.update(is_read=False)
        self.message_user(request, f'{updated} mesaje au fost marcate ca necitite.')
    mark_as_unread.short_description = 'Marchează ca necitite'

    def get_short_message(self, obj):
        return obj.get_short_message()
    get_short_message.short_description = 'Mesaj'

    def has_add_permission(self, request):
        # Prevent manual addition of contact messages
        return False


@admin.register(ContactSettings)
class ContactSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Informații companie', {
            'fields': ('company_name', 'address', 'phone', 'email', 'description')
        }),
        ('Program de lucru', {
            'fields': ('monday_friday_hours', 'saturday_hours', 'sunday_hours'),
            'description': 'Configurați programul de lucru pentru fiecare zi a săptămânii'
        }),
        ('Rețele sociale', {
            'fields': ('facebook_url', 'instagram_url', 'youtube_url'),
            'classes': ('collapse',)
        }),
        ('Hartă', {
            'fields': ('map_embed_code',),
            'classes': ('collapse',),
            'description': 'Codul iframe pentru harta Google Maps (opțional)'
        }),
        ('Informații sistem', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    readonly_fields = ['created_at', 'updated_at']

    def has_add_permission(self, request):
        # Only allow one instance of ContactSettings
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        # Prevent deletion of the only instance
        return False
