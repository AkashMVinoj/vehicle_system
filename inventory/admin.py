from django.contrib import admin
from .models import Vehicle, Booking

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'brand', 'year', 'fuel_type', 'price_per_day', 'is_available')
    list_filter = ('fuel_type', 'is_available', 'brand')
    search_fields = ('name', 'brand')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'vehicle', 'customer_name', 'customer_phone', 'start_date', 'end_date', 'total_amount')
    list_filter = ('start_date', 'end_date')
    search_fields = ('customer_name', 'customer_phone', 'vehicle__name')