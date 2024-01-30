from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import WebsiteViewSet

router = DefaultRouter()
router.register(r'websites', WebsiteViewSet, basename='websites')

urlpatterns = [
    path('', include(router.urls)),
]