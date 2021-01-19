from rest_framework import serializers
from .models import Car, Reservation

class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ['id', 'brand', 'model', 'registration_number', 'date_of_next_technical_examination']

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ['reservating_person', 'reservation_date_from', 'reservation_date_to', 'booked_car']


"""
    brand = serializers.CharField(max_length=50)
    model = serializers.CharField(max_length=50)
    registration_number = serializers.CharField(max_length=15)
    date_of_next_technical_examination = serializers.DateField()

    def create(self, validated_data):
        return Car.objects.create(validated_data)

    def update(self, instance, validated_data):
        instance.brand = validated_data.get('title', instance.title)
        instance.model = validated_data.get('model', instance.model)
        instance.registration_number = validated_data.get('registration_number', instance.registration_number)
        instance.date_of_next_technical_examination = validated_data.get('date_of_next_technical_examination',
                                                                         instance.date_of_next_technical_examination)
        instance.save()
        return instance
"""