from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import CDNViewSet,DomainViewSet, HostingCategoryViewSet, HostingViewSet, ServiceProviderViewSet, UnavailableLogViewSet, WebsiteCategoryViewSet, WebsiteViewSet

router = DefaultRouter()
router.register(r'cdns', CDNViewSet)
router.register(r'domains', DomainViewSet)
router.register(r'hosting-categories', HostingCategoryViewSet)
router.register(r'hostings', HostingViewSet)
router.register(r'service-providers', ServiceProviderViewSet)
router.register(r'unavailable-log', UnavailableLogViewSet)
router.register(r'website-categories', WebsiteCategoryViewSet)
router.register(r'websites', WebsiteViewSet)

urlpatterns = [
    path('', include(router.urls)),
]