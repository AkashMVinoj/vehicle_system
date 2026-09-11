from datetime import date, timedelta
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Vehicle, Booking

class VehicleBookingAPITests(APITestCase):

    def setUp(self):
        self.vehicle1 = Vehicle.objects.create(
            name="Innova Crysta",
            brand="Toyota",
            year=2024,
            price_per_day="2500.00",
            fuel_type="Diesel",
            is_available=True
        )
        self.vehicle2 = Vehicle.objects.create(
            name="Model 3",
            brand="Tesla",
            year=2023,
            price_per_day="5000.00",
            fuel_type="Electric",
            is_available=True
        )

    # ------------------ Vehicle Tests ------------------ #
    def test_create_vehicle(self):
        data = {
            "name": "Nexon EV",
            "brand": "Tata",
            "year": 2024,
            "price_per_day": "1800.00",
            "fuel_type": "Electric",
            "is_available": True
        }
        response = self.client.post('/api/vehicles/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Vehicle.objects.count(), 3)

    def test_list_vehicles(self):
        response = self.client.get('/api/vehicles/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_vehicle_details(self):
        response = self.client.get(f'/api/vehicles/{self.vehicle1.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Innova Crysta")

    def test_update_vehicle(self):
        data = {
            "name": "Innova Crysta VX",
            "brand": "Toyota",
            "year": 2024,
            "price_per_day": "2700.00",
            "fuel_type": "Diesel",
            "is_available": True
        }
        response = self.client.put(f'/api/vehicles/{self.vehicle1.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Innova Crysta VX")

    def test_delete_vehicle(self):
        response = self.client.delete(f'/api/vehicles/{self.vehicle1.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_filter_vehicles_by_brand(self):
        response = self.client.get('/api/vehicles/?brand=Toyota')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_filter_vehicles_by_fuel_type(self):
        response = self.client.get('/api/vehicles/?fuel_type=Electric')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    # ------------------ Booking Tests ------------------ #
    def test_successful_booking_and_auto_calculation(self):
        start = date.today() + timedelta(days=10)
        end = date.today() + timedelta(days=13)  # 3 days
        
        booking_data = {
            "vehicle": self.vehicle1.id,
            "customer_name": "Akash M Vinoj",
            "customer_phone": "9207135723",
            "start_date": start.strftime('%Y-%m-%d'),
            "end_date": end.strftime('%Y-%m-%d')
        }
        response = self.client.post('/api/bookings/', booking_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(float(response.data['total_amount']), 7500.0)

        # Vehicle becomes unavailable test
        self.vehicle1.refresh_from_db()
        self.assertFalse(self.vehicle1.is_available)

    def test_past_start_date_rejection(self):
        past_date = date.today() - timedelta(days=2)
        end = date.today() + timedelta(days=2)
        
        booking_data = {
            "vehicle": self.vehicle1.id,
            "customer_name": "Test User",
            "customer_phone": "9207135723",
            "start_date": past_date.strftime('%Y-%m-%d'),
            "end_date": end.strftime('%Y-%m-%d')
        }
        response = self.client.post('/api/bookings/', booking_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('start_date', response.data)

    def test_invalid_end_date_rejection(self):
        start = date.today() + timedelta(days=10)
        end = start - timedelta(days=2)
        
        booking_data = {
            "vehicle": self.vehicle1.id,
            "customer_name": "Test User",
            "customer_phone": "9207135723",
            "start_date": start.strftime('%Y-%m-%d'),
            "end_date": end.strftime('%Y-%m-%d')
        }
        response = self.client.post('/api/bookings/', booking_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('end_date', response.data)

    def test_invalid_phone_number_rejection(self):
        start = date.today() + timedelta(days=5)
        end = date.today() + timedelta(days=8)
        
        booking_data = {
            "vehicle": self.vehicle1.id,
            "customer_name": "Test User",
            "customer_phone": "920713572",  # 9 digits
            "start_date": start.strftime('%Y-%m-%d'),
            "end_date": end.strftime('%Y-%m-%d')
        }
        response = self.client.post('/api/bookings/', booking_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('customer_phone', response.data)

    def test_overlapping_booking_rejection(self):
        start1 = date.today() + timedelta(days=10)
        end1 = date.today() + timedelta(days=15)
        
        Booking.objects.create(
            vehicle=self.vehicle1,
            customer_name="Customer 1",
            customer_phone="9207135723",
            start_date=start1,
            end_date=end1,
            total_amount=12500.0
        )

        # Overlapping attempt (12 to 17)
        start2 = date.today() + timedelta(days=12)
        end2 = date.today() + timedelta(days=17)
        
        booking_data = {
            "vehicle": self.vehicle1.id,
            "customer_name": "Customer 2",
            "customer_phone": "9876543210",
            "start_date": start2.strftime('%Y-%m-%d'),
            "end_date": end2.strftime('%Y-%m-%d')
        }
        response = self.client.post('/api/bookings/', booking_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('vehicle', response.data)