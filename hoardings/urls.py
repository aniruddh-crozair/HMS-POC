from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HoardingImageViewSet, GeoTagViewSet, HoardingViewSet, index, hoarding_map

router = DefaultRouter()
router.register(r'images', HoardingImageViewSet)
router.register(r'geotags', GeoTagViewSet)
router.register(r'hoardings', HoardingViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('', index, name="index"),
    path('map/', hoarding_map, name='hoarding_map'),
]