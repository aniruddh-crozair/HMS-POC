from rest_framework import viewsets
from .models import Hoarding, GeoTag, HoardingImage, Customer, Booking
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
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
    """Render the map page"""
    return render(request, "map.html") 


def book_hoarding(request, hoarding_id):
    """
    Books the hoarding for customer.
    Args:
        hoarding_id (int): UUID of hoarding
    Returns:
        None
    """
    hoarding = get_object_or_404(Hoarding, id=hoarding_id)

    if request.method == 'POST':
        customer_name = request.POST.get('name')
        customer_email = request.POST.get('email')
        customer_phone = request.POST.get('phone')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        # Get or create the customer
        customer, created = Customer.objects.get_or_create(
            email = customer_email,
            defaults = {
                "name": customer_name,
                "phone": customer_phone
            }
        )

        # Create the booking of hoarding
        Booking.objects.create(
            hoarding = hoarding,
            customer = customer,
            start_date = start_date,
            end_date = end_date,
        )

        return HttpResponse('Hoarding Booked successfully')
    return render(request, "book_hoarding.html", {'hoarding': hoarding})