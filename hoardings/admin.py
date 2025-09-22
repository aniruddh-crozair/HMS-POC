from django.contrib import admin
from .models import (Hoarding, 
                     GeoTag, 
                     HoardingImage, 
                     Customer, 
                     Booking)

admin.site.register(Hoarding)
admin.site.register(GeoTag)
admin.site.register(HoardingImage)
admin.site.register(Customer)
admin.site.register(Booking)
