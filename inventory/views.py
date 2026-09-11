from rest_framework import viewsets, mixins, filters
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .models import Vehicle, Booking
from .serializers import VehicleSerializer, BookingSerializer

# -------------------------------------------------------------------
# Frontend Views (HTML Page Rendering)
# -------------------------------------------------------------------

def frontend_home(request):
    """
    Renders the Vehicle Management Panel (Admin Dashboard)
    """
    return render(request, 'inventory/index.html')


def booking_view(request):
    """
    Renders the Customer Booking Portal
    """
    return render(request, 'inventory/booking.html')


# -------------------------------------------------------------------
# REST API ViewSets
# -------------------------------------------------------------------

@method_decorator(csrf_exempt, name='dispatch')
class VehicleViewSet(viewsets.ModelViewSet):
    """
    ViewSet for full CRUD operations on Vehicles.
    Supports filtering and searching by brand, fuel_type, name, and availability.
    """
    queryset = Vehicle.objects.all().order_by('-id')
    serializer_class = VehicleSerializer
    permission_classes = [AllowAny]
    authentication_classes = []
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['brand', 'fuel_type', 'is_available']
    search_fields = ['brand', 'name']


@method_decorator(csrf_exempt, name='dispatch')
class BookingViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    """
    ViewSet for listing, retrieving, and creating Bookings.
    """
    queryset = Booking.objects.all().order_by('-id')
    serializer_class = BookingSerializer
    permission_classes = [AllowAny]
    authentication_classes = []