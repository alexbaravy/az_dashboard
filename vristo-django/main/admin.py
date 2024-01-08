from django.contrib import admin
from django.contrib.admin import AdminSite

from django.utils.html import format_html
from .models import ServiceProvider
from .models import Domain, Hosting, HostingCategory, CDN
from .models import Website, WebsiteCategory
from .widgets import CustomTextInput


class MainAdminSite(AdminSite):
    site_header = "AZ Dashboard"
    site_title = "Admin Panel"
    index_title = "Admin Panel"

    def get_app_list(self, request):
        ordering = {
            'Service providers': 1,
            'Hosting categories': 2,
            'Website categories': 3,
            'Domains': 5,
            'Hostings': 5,
            'CDN Providers': 6,
            'Websites': 7
        }

        app_dict = self._build_app_dict(request)
        app_list = sorted(app_dict.values(), key=lambda x: x['name'].lower())

        # Sort the models alphabetically within each app.
        for app in app_list:
            app['models'].sort(key=lambda x: ordering[x['name']])

        return app_list


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

    # class Meta:
    #     widgets = {
    #         'url': CustomTextInput(),
    #         'service_provider': CustomTextInput(),
    #         'start_date': CustomTextInput(),
    #         'end_date': CustomTextInput(),
    #         'check_enabled': CustomTextInput(),
    #         'deactivated': CustomTextInput(),
    #         'url': CustomTextInput(),
    #     }


class HostingCategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


class HostingAdmin(admin.ModelAdmin):
    fields = ['ip', 'category', 'service_provider', 'start_date', 'end_date', 'login', 'password', 'note']
    list_display = ['ip', 'start_date', 'end_date', 'login', 'password', 'note']
    search_fields = ['ip', 'start_date', 'end_date', 'login', 'password', 'note']


class CDNAdmin(admin.ModelAdmin):
    fields = ['ip', 'service_provider', 'start_date', 'end_date', 'login', 'password', 'note']
    list_display = ['ip', 'start_date', 'end_date', 'login', 'password', 'note']
    search_fields = ['ip', 'start_date', 'end_date', 'login', 'password', 'note']


class WebsiteCategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


class WebsiteAdmin(admin.ModelAdmin):
    fields = ['name', 'category', 'domain', 'hosting', 'cdn', 'note']
    list_display = ['name', 'category', 'domain', 'hosting', 'cdn', 'note']
    search_fields = ['name', 'category', 'domain', 'hosting', 'cdn', 'note']


main_admin_site = MainAdminSite(name='main_admin')

main_admin_site.register(ServiceProvider, ServiceProviderAdmin)
main_admin_site.register(HostingCategory, HostingCategoryAdmin)
main_admin_site.register(WebsiteCategory, WebsiteCategoryAdmin)

main_admin_site.register(Domain, DomainAdmin)
main_admin_site.register(Hosting, HostingAdmin)
main_admin_site.register(CDN, CDNAdmin)

main_admin_site.register(Website, WebsiteAdmin)
