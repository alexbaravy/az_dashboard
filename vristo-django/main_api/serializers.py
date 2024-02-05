from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from main.models import CDN, Domain, HostingCategory, Hosting, ServiceProvider, UnavailableLog, WebsiteCategory, Website


class CDNSerializer(ModelSerializer):
    service_provider_name = serializers.SerializerMethodField()

    class Meta:
        model = CDN
        fields = ['id', 'service_provider_name', 'ip', 'start_date', 'end_date', 'check_enabled', 'deactivated', 'note']

    def get_service_provider_name(self, obj):
        return obj.service_provider.name


class DomainSerializer(ModelSerializer):
    service_provider_name = serializers.SerializerMethodField()

    class Meta:
        model = Domain
        fields = ['id', 'service_provider_name', 'url', 'start_date', 'end_date', 'check_enabled', 'deactivated',
                  'note']

    def get_service_provider_name(self, obj):
        return obj.service_provider.name


class HostingCategorySerializer(ModelSerializer):
    class Meta:
        model = HostingCategory
        fields = '__all__'


class HostingSerializer(ModelSerializer):
    service_provider_name = serializers.SerializerMethodField()
    category_name = serializers.SerializerMethodField()

    class Meta:
        model = Hosting
        fields = ['id', 'service_provider_name', 'category_name', 'start_date', 'end_date', 'check_enabled',
                  'deactivated', 'note']

    def get_service_provider_name(self, obj):
        return obj.service_provider.name

    def get_category_name(self, obj):
        return obj.category.name


class ServiceProviderSerializer(ModelSerializer):
    class Meta:
        model = ServiceProvider
        fields = ['id', 'name', 'url', 'note']


class UnavailableLogSerializer(ModelSerializer):
    domain_name = serializers.SerializerMethodField()

    class Meta:
        model = UnavailableLog
        fields = ['id', 'domain_name', 'start_date', 'end_date', 'start_status', 'end_status']

    def get_domain_name(self, obj):
        return obj.website.domain.url


class WebsiteCategorySerializer(ModelSerializer):
    class Meta:
        model = WebsiteCategory
        fields = '__all__'


class WebsiteSerializer(ModelSerializer):
    category_name = serializers.SerializerMethodField()
    domain_url = serializers.SerializerMethodField()
    hosting_ip = serializers.SerializerMethodField()
    cdn_ip = serializers.SerializerMethodField()

    class Meta:
        model = Website
        fields = ['id', 'name', 'check_enabled', 'deactivated', 'note', 'category_name', 'domain_url',
                  'hosting_ip', 'cdn_ip']

    def get_category_name(self, obj):
        return obj.category.name

    def get_domain_url(self, obj):
        return obj.domain.url

    def get_hosting_ip(self, obj):
        return obj.hosting.ip

    def get_cdn_ip(self, obj):
        if obj.cdn:
            return obj.cdn.ip
        return None
