from .models import Car, Reservation
from .serializers import CarSerializer, ReservationSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets, permissions


class CarList(APIView):
    """
    List all cars
    """

    def get(self, request, format=None):
        cars = Car.objects.all()
        serializer = CarSerializer(cars, many=True)
        return Response(serializer.data)


class CarDetail(APIView):
    """
    Create, retrieve, update or delete a car instance.
    """

    def get_object(self, pk):  # !TODO: getobjector404 lepsze?
        try:
            return Car.objects.get(pk=pk)
        except Car.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        cars = self.get_object(pk)
        serializer = CarSerializer(cars)
        return Response(serializer.data)

    def post(self, request, pk, format=None):
        serializer = CarSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format=None):
        car = self.get_object(pk)
        serializer = CarSerializer(car, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        car = self.get_object(pk)
        car.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ReservationList(APIView):
    """
    List all reservations for specific car or creates new reservation
    """

    def get_car(self, pk):  # !TODO: getobjector404 lepsze?
        try:
            return Car.objects.get(pk=pk)
        except Car.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        reserved_car = self.get_car(pk)
        reservations = [reservation for reservation in Reservation.objects.filter(booked_car=reserved_car)]
        serializer = ReservationSerializer(reservations, many=True)
        return Response(serializer.data)

    def post(self, request, pk, format=None):
        reservation_to_create = {
            'reservating_person' : request.data['reservating_person'],
            'reservation_date_from' : request.data['reservation_date_from'],
            'reservation_date_to' : request.data['reservation_date_to'],
            'booked_car' : pk
        }

        serializer = ReservationSerializer(data=reservation_to_create, many=False)
        if serializer.is_valid():
            serializer.save()
            return Response(reservation_to_create, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
