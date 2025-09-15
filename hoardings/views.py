from rest_framework import viewsets
from .models import Hoarding, GeoTag, HoardingImage
from django.shortcuts import render, redirect, HttpResponse
from .serializers import HoardingSerializer, GeoTagSerializer, HoardingImageSerializer

class HoardingImageViewSet(viewsets.ModelViewSet):
    queryset = HoardingImage.objects.all().order_by('-created_at')
    serializer_class = HoardingImageSerializer


class GeoTagViewSet(viewsets.ModelViewSet):
    queryset = GeoTag.objects.all().order_by('-captured_at')
    serializer_class = GeoTagSerializer

class HoardingViewSet(viewsets.ModelViewSet):
    queryset = Hoarding.objects.all().order_by('-created_at')
    serializer_class = HoardingSerializer



def index(request):
    """
    Handle hoarding creation with user-submitted data.
    Args:
        request (HttpRequest): The HTTP request containing form data.
    Returns:
        HttpResponse: A success message once data is saved.
    """

    # Ensure the request is POST
    if request.method == 'POST':
        # Extract form fields
        title = request.POST.get('title')
        description = request.POST.get('description')
        price = request.POST.get('price')
        image = request.FILES.get('image')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')

        # Create the main hoarding record
        hoarding = Hoarding.objects.create(
            title=title,
            description=description,
            price=price if price else None,
        )

        # Save location if available
        if latitude and longitude:
            GeoTag.objects.create(
                hoarding=hoarding,
                latitude=latitude,
                longitude=longitude,
            )

        # Save image if uploaded
        if image:
            HoardingImage.objects.create(
                hoarding=hoarding,
                image=image,
            )

        return redirect("hoarding_map")
    
    return render(request, "index.html")


def hoarding_map(request):
    return render(request, "map.html") 