from rest_framework import viewsets
from main.models import Website
from .serializers import WebsiteSerializer
class WebsiteViewSet(viewsets.ModelViewSet):
    queryset = Website.objects.all()
    serializer_class = WebsiteSerializer