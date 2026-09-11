from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VehicleViewSet, BookingViewSet  # നിങ്ങളുടെ ViewSet പേരുകൾ

router = DefaultRouter()
router.register(r'vehicles', VehicleViewSet, basename='vehicle')
router.register(r'bookings', BookingViewSet, basename='booking')

urlpatterns = [
    path('', include(router.urls)),
]