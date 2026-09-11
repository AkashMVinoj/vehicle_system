from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils import timezone

class Vehicle(models.Model):
    FUEL_CHOICES = [
        ('Petrol', 'Petrol'),
        ('Diesel', 'Diesel'),
        ('Electric', 'Electric'),
        ('Hybrid', 'Hybrid'),
    ]

    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    year = models.IntegerField()
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    fuel_type = models.CharField(max_length=20, choices=FUEL_CHOICES)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.brand} {self.name} ({self.year})"


class Booking(models.Model):
    phone_validator = RegexValidator(
        regex=r'^\d{10}$',
        message="Phone number must be exactly 10 digits."
    )

    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='bookings')
    customer_name = models.CharField(max_length=100)
    customer_phone = models.CharField(max_length=10, validators=[phone_validator])
    start_date = models.DateField()
    end_date = models.DateField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def clean(self):
        # 1. Start date cannot be in the past
        if self.start_date and self.start_date < timezone.now().date():
            raise ValidationError({'start_date': "Start date cannot be in the past."})

        # 2. End date must be after start date
        if self.start_date and self.end_date and self.end_date <= self.start_date:
            raise ValidationError({'end_date': "End date must be after the start date."})

        # 3. Check overlapping dates for the same vehicle
        if self.vehicle and self.start_date and self.end_date:
            overlapping_bookings = Booking.objects.filter(
                vehicle=self.vehicle,
                start_date__lt=self.end_date,
                end_date__gt=self.start_date
            ).exclude(pk=self.pk)

            if overlapping_bookings.exists():
                raise ValidationError("This vehicle is already booked for the selected date range.")

    def save(self, *args, **kwargs):
        # Run clean validation rules before saving
        self.full_clean()

        # Auto-calculate total_amount (days * price_per_day)
        days = (self.end_date - self.start_date).days
        self.total_amount = days * self.vehicle.price_per_day

        super().save(*args, **kwargs)

        # Update vehicle availability state
        self.vehicle.is_available = False
        self.vehicle.save(update_fields=['is_available'])