import uuid
from django.db import models
from django.utils import timezone
from datetime import timedelta

# Note
# 1. Comment for each line
# 2. Well structured space for each code 
# 3. Doc string before each class and function and section 


class Hoarding(models.Model):
    """
    Represent a hoarding (advertisement board).

    Store details like title, description, price, rating
    and keeps track of creation/update timestamps.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Returns the title if available, otherwise the UUID."""
        return self.title or str(self.id)
    
    @property
    def status(self):
        """
        Return the booking status and color for the hoarding.
            - Red: Booked for more than 7 days or may be for months.
            - Orange: Booked but ending within 7 days.
            - Green: Currently unbooked.
        """
        current_booking = self.bookings.filter(
            start_date__lte = timezone.now(),
            end_date__gte = timezone.now()
        ).first()

        if current_booking:
            if current_booking.end_date <= (timezone.now() + timedelta(days=7)).date():
                return "Orange"
            return "Red"
        return "Green"
    

class GeoTag(models.Model):
    """
    Represents a geographical tag for a hoarding.

    Stores latitude, longitude, and optional address details.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) 
    hoarding = models.ForeignKey(Hoarding, related_name='geotags', on_delete=models.CASCADE)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    address = models.TextField(blank=True, null=True)
    captured_at = models.DateTimeField(auto_now_add=True)

class HoardingImage(models.Model):
    """
    Represents an image associated with a hoarding.

    Stores the image file and optional metadata.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) 
    hoarding = models.ForeignKey(Hoarding, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to="hoarding_images/")
    metadata = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Customer(models.Model):
    """
    Represents a customer who can book hoardings.

    Stores basic contact details like name, email, and phone.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        """Return the customer's name."""
        return self.name
    

class Booking(models.Model):
    """
    Represents a booking made by a customer for a hoarding.

    Stores start and end dates along with references to
    the customer and the hoarding.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    hoarding = models.ForeignKey(Hoarding, related_name='bookings', on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, related_name='bookings', on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return a string showing which customer booked which hoarding."""
        return f"{self.customer.name} → {self.hoarding.title}"