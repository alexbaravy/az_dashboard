from rest_framework import viewsets
from main.models import CDN, Domain, HostingCategory, Hosting, ServiceProvider, UnavailableLog, WebsiteCategory, Website
from .serializers import CDNSerializer, DomainSerializer, HostingCategorySerializer, HostingSerializer, \
    ServiceProviderSerializer, UnavailableLogSerializer, WebsiteCategorySerializer, WebsiteSerializer


class CDNViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CDN.objects.all()
    serializer_class = CDNSerializer


class DomainViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Domain.objects.all()
    serializer_class = DomainSerializer


class HostingCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = HostingCategory.objects.all()
    serializer_class = HostingCategorySerializer


class HostingViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Hosting.objects.all()
    serializer_class = HostingSerializer


class ServiceProviderViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ServiceProvider.objects.all()
    serializer_class = ServiceProviderSerializer


class UnavailableLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = UnavailableLog.objects.all()
    serializer_class = UnavailableLogSerializer


class WebsiteCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = WebsiteCategory.objects.all()
    serializer_class = WebsiteCategorySerializer


class WebsiteViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Website.objects.all()
    serializer_class = WebsiteSerializer
