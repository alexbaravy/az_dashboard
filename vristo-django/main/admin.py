from django.contrib import admin
from django.contrib.admin import AdminSite
from django.utils.html import format_html
from .models import ServiceProvider
from .models import Domain, Hosting, HostingCategory, CDN
from .models import Website, WebsiteCategory
from .models import UnavailableLog
from .widgets import CustomTextInput


class ServiceProviderAdmin(admin.ModelAdmin):
    fields = ['name', 'url', 'login', 'password', 'note']
    list_display = ['name', 'display_url', 'login', 'password', 'note']
    search_fields = ['name', 'url', 'login', 'password', 'note']

    def display_url(self, obj):
        return format_html(f'<a href={obj.url}>{obj.url}</a>')

    display_url.short_description = 'url'


class DomainAdmin(admin.ModelAdmin):
    fields = ['url', 'service_provider', 'start_date', 'end_date', 'check_enabled', 'deactivated', 'note']
    list_display = ['url', 'start_date', 'end_date', 'note']
    search_fields = ['url', 'start_date', 'end_date', 'note']


class HostingCategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


class HostingAdmin(admin.ModelAdmin):
    fields = ['ip', 'category', 'service_provider', 'start_date', 'end_date', 'login', 'password', 'check_enabled',
              'deactivated', 'note']
    list_display = ['ip', 'start_date', 'end_date', 'login', 'password', 'note']
    search_fields = ['ip', 'start_date', 'end_date', 'login', 'password', 'note']


class CDNAdmin(admin.ModelAdmin):
    fields = ['ip', 'service_provider', 'start_date', 'end_date', 'login', 'password', 'check_enabled', 'deactivated',
              'note']
    list_display = ['ip', 'start_date', 'end_date', 'login', 'password', 'note']
    search_fields = ['ip', 'start_date', 'end_date', 'login', 'password', 'note']


class WebsiteCategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


class WebsiteAdmin(admin.ModelAdmin):
    fields = ['name', 'category', 'domain', 'hosting', 'cdn', 'check_enabled', 'deactivated', 'note']
    list_display = ['name', 'category', 'domain', 'hosting', 'cdn', 'domain_hash', 'note']
    search_fields = ['name', 'category', 'domain', 'hosting', 'cdn', 'note']


class UnavailableLogAdmin(admin.ModelAdmin):
    fields = ['website', 'start_date', 'end_date', 'start_status', 'end_status']
    list_display = ['website', 'start_date', 'end_date', 'start_status', 'end_status']
    search_fields = ['website', 'start_date', 'end_date', 'start_status', 'end_status']


admin.site.register(ServiceProvider, ServiceProviderAdmin)
admin.site.register(HostingCategory, HostingCategoryAdmin)
admin.site.register(WebsiteCategory, WebsiteCategoryAdmin)

admin.site.register(Domain, DomainAdmin)
admin.site.register(Hosting, HostingAdmin)
admin.site.register(CDN, CDNAdmin)

admin.site.register(Website, WebsiteAdmin)
admin.site.register(UnavailableLog, UnavailableLogAdmin)
