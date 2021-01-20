from .models import Car, Reservation
from .serializers import CarSerializer, ReservationSerializer, MiniReservationSerializer, \
    ReservationWithDetailsSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets, permissions
from django.shortcuts import get_object_or_404
from datetime import datetime


class AuxiliaryMethods():
    """
    Methods, which implements logic into API
    """

    @staticmethod
    def get_reservations(car):
        """
        :param car: should be an object of class Car
        :return: Returns list of reservations of the specific car
        """

        return [reservation for reservation in Reservation.objects.filter(booked_car=car)]

    @staticmethod
    def is_period_valid(list_of_reservations, new_from, new_to, next_technical_examination):
        """
        The method checks if new reservation date dosen't collide with existing ones
        :param next_technical_examination:
        :param list_of_reservations: should be a list of tuples [(date_of_start_reservation, date_of_end_reservation)]
        :param new_from: this is date when new reservation starts
        :param new_to: this is date when new reservation ends
        :param next_technical_examination: It is needed to check if reservations ends before technical examination
        """

        # Converts string into datetime object
        new_date_from = datetime.strptime(new_from, '%Y-%m-%dT%H:%M:%S%z')
        new_date_to = datetime.strptime(new_to, '%Y-%m-%dT%H:%M:%S%z')

        if next_technical_examination >= new_date_to.date():
            if list_of_reservations:
                if new_from < new_to:
                    for reservation in list_of_reservations:
                        if all(map(lambda x: reservation[1] >= x >= reservation[0], (new_date_from, new_date_to))):
                            return False
                    return True
                else:
                    return False
            else:
                return True
        else:
            return False


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

    def get(self, request, pk):
        cars = get_object_or_404(Car, pk=pk)
        serializer = CarSerializer(cars)
        return Response(serializer.data)

    def post(self, request, pk):
        serializer = CarSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        car = get_object_or_404(Car, pk=pk)
        serializer = CarSerializer(car, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        car = get_object_or_404(Car, pk=pk)
        serializer = CarSerializer(car, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        car = get_object_or_404(Car, pk=pk)
        reservations = AuxiliaryMethods.get_reservations(car)
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

    def get(self, request, pk):
        reserved_car = get_object_or_404(Car, pk=pk)
        reservations = AuxiliaryMethods.get_reservations(reserved_car)
        serializer = MiniReservationSerializer(reservations, many=True)
        return Response(serializer.data)

    def post(self, request, pk):
        car = get_object_or_404(Car, pk=pk)

        # Prepares data to trasnfer to the serializer
        reservation_to_create = {
            'booking_person': request.data['booking_person'],
            'reservation_date_from': request.data['reservation_date_from'],
            'reservation_date_to': request.data['reservation_date_to'],
            'booked_car': pk
        }

        # Creates a list of tuples with dates of reservations
        dates_of_reservations = []
        for reservation in AuxiliaryMethods.get_reservations(car):
            dates_of_reservations.append((reservation.reservation_date_from, reservation.reservation_date_to))

        # Checks if date of new reservations doesn't collide with others and saves in DB
        if AuxiliaryMethods.is_period_valid(dates_of_reservations, request.data['reservation_date_from'],
                                            request.data['reservation_date_to'],
                                            car.date_of_next_technical_examination):
            serializer = ReservationSerializer(data=reservation_to_create, many=False)
            if serializer.is_valid():
                serializer.save()
                return Response(reservation_to_create, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("You can't post this reservation due to one of the followings reason: "
                            "1) There is another reservation is this time "
                            "2) Reservation ends earlier than starts! "
                            "3) In this period car's technical examination is planned",
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)


class ReservationDetails(APIView):
    """
    shows details of specific reservation, edits or deletes it
    """

    def get(self, request, pk, pk2):
        reservation = get_object_or_404(Reservation, pk=pk2)
        serializer = ReservationWithDetailsSerializer(reservation, many=False)
        return Response(serializer.data)

    def put(self, request, pk, pk2):
        reservation = get_object_or_404(Reservation, pk=pk2)
        serializer = ReservationWithDetailsSerializer(reservation, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, pk2):
        reservation = get_object_or_404(Reservation, pk=pk2)
        serializer = ReservationWithDetailsSerializer(reservation, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, pk2):
        reservation = get_object_or_404(Reservation, pk=pk2)
        reservation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
