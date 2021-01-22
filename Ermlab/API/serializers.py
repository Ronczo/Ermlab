from rest_framework import serializers
from .models import Car, Reservation


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ['id', 'brand', 'model', 'registration_number', 'date_of_next_technical_examination']


class MiniReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ['id', 'booking_person', 'date_from', 'date_to']


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ['id', 'booking_person', 'date_from', 'date_to', 'booked_car']


class ReservationWithDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ['id', 'booking_person', 'date_from', 'date_to', 'booked_car']
        depth = 1
