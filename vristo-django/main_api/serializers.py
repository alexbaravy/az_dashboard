from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from main.models import Website


class WebsiteSerializer(ModelSerializer):
    class Meta:
        model = Website
        fields = '__all__'
