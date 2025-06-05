from django.contrib import admin
from .models import SiteSettings, County, Lake, Video, HeroSection, FooterSettings

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

@admin.register(Lake)
class LakeAdmin(admin.ModelAdmin):
    list_display = ['name', 'county', 'price_per_day', 'is_active', 'created_at']
    list_filter = ['county', 'is_active', 'created_at']
    search_fields = ['name', 'description', 'fish_types', 'address', 'rules']
    readonly_fields = ['created_at', 'updated_at']
    list_editable = ['is_active']
    list_per_page = 20

    fieldsets = (
        ('Informații de bază', {
            'fields': ('name', 'county', 'address', 'description')
        }),
        ('Localizare', {
            'fields': ('latitude', 'longitude'),
            'description': 'Coordonatele GPS ale lacului. Poți găsi coordonatele pe Google Maps făcând click dreapta pe locație.'
        }),
        ('Detalii pescuit', {
            'fields': ('fish_types', 'facilities', 'price_per_day', 'rules')
        }),
        ('Media și vizibilitate', {
            'fields': ('image', 'is_active')
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
