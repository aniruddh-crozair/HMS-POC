from django.contrib import admin
from .models import Hoarding, GeoTag, HoardingImage

admin.site.register(Hoarding)
admin.site.register(GeoTag)
admin.site.register(HoardingImage)
