from django.contrib import admin
from .models import SiteSettings, County, Lake, Video

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        # Only allow one instance of SiteSettings
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        # Prevent deletion of the only instance
        return False

@admin.register(County)
class CountyAdmin(admin.ModelAdmin):
    list_display = ['name', 'region', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'region']

@admin.register(Lake)
class LakeAdmin(admin.ModelAdmin):
    list_display = ['name', 'county', 'price_per_day', 'is_active']
    list_filter = ['county', 'is_active']
    search_fields = ['name', 'description', 'fish_types']

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active', 'is_featured', 'created_at']
    list_filter = ['is_active', 'is_featured']
    search_fields = ['title', 'description']
