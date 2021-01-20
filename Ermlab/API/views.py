from .models import Car, Reservation
from .serializers import CarSerializer, ReservationSerializer, MiniReservationSerializer
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

    def get_car(self, pk):  # !TODO: getobjector404 lepsze?
        try:
            return Car.objects.get(pk=pk)
        except Car.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        cars = self.get_car(pk)
        serializer = CarSerializer(cars)
        return Response(serializer.data)

    def post(self, request, pk):
        serializer = CarSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        car = self.get_car(pk)
        serializer = CarSerializer(car, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        car = self.get_car(pk)
        serializer = CarSerializer(car, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        car = self.get_car(pk)
        reservations = [reservation for reservation in Reservation.objects.filter(booked_car=car)]
        if reservations:
            return Response("You can't delete this car. There are reservations for this car",
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
        else:
            car.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


class ReservationList(APIView):
    """
    List all reservations for specific car or creates new reservation for specific car
    """

    def get_car(self, pk):  # !TODO: getobjector404 lepsze?
        try:
            return Car.objects.get(pk=pk)
        except Car.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        reserved_car = self.get_car(pk)
        reservations = [reservation for reservation in Reservation.objects.filter(booked_car=reserved_car)]
        serializer = MiniReservationSerializer(reservations, many=True)
        return Response(serializer.data)

    def post(self, request, pk):
        reservation_to_create = {
            'booking_person' : request.data['booking_person'],
            'reservation_date_from' : request.data['reservation_date_from'],
            'reservation_date_to' : request.data['reservation_date_to'],
            'booked_car' : pk
        }

        serializer = ReservationSerializer(data=reservation_to_create, many=False)
        if serializer.is_valid():
            serializer.save()
            return Response(reservation_to_create, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ReservationDetails(APIView):
    """
    shows details of specific reservation, edits or deletes it
    """

    def get_car(self, pk):  # !TODO: getobjector404 lepsze?
        try:
            return Car.objects.get(pk=pk)
        except Car.DoesNotExist:
            raise Http404

    def get_reservation(self, pk):  # !TODO: getobjector404 lepsze?
        try:
            return Reservation.objects.get(pk=pk)
        except Reservation.DoesNotExist:
            raise Http404

    def get(self, request, pk, pk2):
        reservation = self.get_reservation(pk2)
        serializer = ReservationSerializer(reservation, many=False)
        return Response(serializer.data)

    def put(self, request, pk, pk2):
        reservation = self.get_reservation(pk2)
        serializer = ReservationSerializer(reservation, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, pk2):
        reservation = self.get_reservation(pk2)
        serializer = ReservationSerializer(reservation, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, pk2):
        reservation = self.get_reservation(pk2)
        reservation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
