from rest_framework import serializers
from .models import Hoarding, GeoTag, HoardingImage


from rest_framework import serializers
from .models import Hoarding, GeoTag, HoardingImage


class HoardingImageSerializer(serializers.ModelSerializer):
    """Serializer for the HoardingImage model."""

    class Meta:
        """Meta configuration for HoardingImageSerializer."""

        model = HoardingImage
        fields = ["id", "hoarding", "image", "metadata", "created_at"]


class GeoTagSerializer(serializers.ModelSerializer):
    """Serializer for the GeoTag model."""

    class Meta:
        """Meta configuration for GeoTagSerializer."""

        model = GeoTag
        fields = [
            "id",
            "hoarding",
            "latitude",
            "longitude",
            "address",
            "captured_at",
        ]


class HoardingSerializer(serializers.ModelSerializer):
    """
    Serializer for the Hoarding model.

    Includes related geotags, images, and computed status.
    """

    geotags = GeoTagSerializer(many=True, read_only=True)
    images = HoardingImageSerializer(many=True, read_only=True)
    status = serializers.ReadOnlyField()

    class Meta:
        """Meta configuration for HoardingSerializer."""

        model = Hoarding
        fields = [
            "id",
            "title",
            "description",
            "price",
            "rating",
            "created_at",
            "updated_at",
            "geotags",
            "images",
            "status",
        ]
