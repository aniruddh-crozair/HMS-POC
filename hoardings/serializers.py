from rest_framework import serializers
from .models import Hoarding, GeoTag, HoardingImage

class HoardingImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = HoardingImage
        fields = ['id', 'hoarding', 'image', 'metadata', 'created_at']

class GeoTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeoTag
        fields = ['id', 'hoarding', 'latitude', 'longitude', 'address', 'captured_at']

class HoardingSerializer(serializers.ModelSerializer):
    geotags = GeoTagSerializer(many=True, read_only=True)
    images = HoardingImageSerializer(many=True, read_only=True)
    status = serializers.ReadOnlyField()
    class Meta:
        model = Hoarding
        fields = ['id', 'title', 'description', 'price', 'rating', 'created_at', 'updated_at', 'geotags', 'images', 'status']