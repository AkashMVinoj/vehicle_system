import re
from datetime import date
from rest_framework import serializers
from .models import Vehicle, Booking


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ['id', 'name', 'brand', 'year', 'price_per_day', 'fuel_type', 'is_available']


class BookingSerializer(serializers.ModelSerializer):
    total_amount = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Booking
        fields = ['id', 'vehicle', 'customer_name', 'customer_phone', 'start_date', 'end_date', 'total_amount']

    def validate_customer_phone(self, value):
        # Convert to string and strip whitespace to handle inputs safely
        phone_str = str(value).strip()
        pattern = r'^\d{10}$'
        if not re.match(pattern, phone_str):
            raise serializers.ValidationError("Customer phone number must contain exactly 10 digits.")
        return phone_str

    def validate(self, attrs):
        vehicle = attrs.get('vehicle')
        start_date = attrs.get('start_date')
        end_date = attrs.get('end_date')

        # 1. Check if start date is in the past
        if start_date and start_date < date.today():
            raise serializers.ValidationError({
                "start_date": "Start date cannot be in the past."
            })

        # 2. Check if end date is after start date
        if start_date and end_date and end_date <= start_date:
            raise serializers.ValidationError({
                "end_date": "End date must be after start date."
            })

        # 3. Check if the vehicle is available
        if vehicle and not vehicle.is_available and not self.instance:
            raise serializers.ValidationError({
                "vehicle": "This vehicle is currently not available for booking."
            })

        # 4. Check for date collision / overlapping bookings
        if vehicle and start_date and end_date:
            overlapping_bookings = Booking.objects.filter(
                vehicle=vehicle,
                start_date__lt=end_date,
                end_date__gt=start_date
            )
            
            if self.instance:
                overlapping_bookings = overlapping_bookings.exclude(pk=self.instance.pk)

            if overlapping_bookings.exists():
                raise serializers.ValidationError({
                    "vehicle": "Vehicle is already booked for the selected dates."
                })

        return attrs

    def create(self, validated_data):
        vehicle = validated_data['vehicle']
        start_date = validated_data['start_date']
        end_date = validated_data['end_date']

        # Calculate total price based on duration
        num_days = (end_date - start_date).days
        total_price = num_days * vehicle.price_per_day
        validated_data['total_amount'] = total_price

        # Save the booking record
        booking = super().create(validated_data)

        # Update vehicle availability status
        vehicle.is_available = False
        vehicle.save()

        return booking