import uuid
from django.db import models
from django.utils import timezone
from datetime import timedelta

class Hoarding(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title or str(self.id)
    
    @property
    def status(self):
        """Return color based on booking status."""
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
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) 
    hoarding = models.ForeignKey(Hoarding, related_name='geotags', on_delete=models.CASCADE)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    address = models.TextField(blank=True, null=True)
    captured_at = models.DateTimeField(auto_now_add=True)

class HoardingImage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) 
    hoarding = models.ForeignKey(Hoarding, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to="hoarding_images/")
    metadata = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Customer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.name
    

class Booking(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    hoarding = models.ForeignKey(Hoarding, related_name='bookings', on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, related_name='bookings', on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer.name} → {self.hoarding.title}"