from django.contrib import admin
from django.utils.html import format_html
from .models import Profile, SiteSettings

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

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'city', 'is_email_verified']
    list_filter = ['is_email_verified']
    search_fields = ['user__email', 'phone', 'city']
    readonly_fields = ['is_email_verified']
