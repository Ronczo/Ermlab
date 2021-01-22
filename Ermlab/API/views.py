from .models import Car, Reservation
from .serializers import CarSerializer, ReservationSerializer, MiniReservationSerializer, \
    ReservationWithDetailsSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db.models.deletion import ProtectedError


class CarList(APIView):
    """
    List all cars instances
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
        try:
            car.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ProtectedError:
            return Response("You can't delete this car. There are reservations for this car",
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)


class ReservationList(APIView):
    """
    List all reservations for specific car or creates new reservation for specific car
    """

    def get(self, request, pk):
        reserved_car = get_object_or_404(Car, pk=pk)
        reservations = Reservation.get_reservations(reserved_car)
        serializer = MiniReservationSerializer(reservations, many=True)
        return Response(serializer.data)

    def post(self, request, pk):
        car = get_object_or_404(Car, pk=pk)

        # Prepares data for serializer
        reservation_to_create = {
            'booking_person': request.data['booking_person'],
            'date_from': request.data['date_from'],
            'date_to': request.data['date_to'],
            'booked_car': pk
        }

        # Checks if date of new reservations doesn't collide with others and saves in DB if it's ok
        if Reservation.is_period_valid(car, request.data['date_from'], request.data['date_to']):
            serializer = ReservationSerializer(data=reservation_to_create, many=False)
            if serializer.is_valid():
                serializer.save()
                return Response(reservation_to_create, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(Reservation.get_reason_of_error(), status=status.HTTP_405_METHOD_NOT_ALLOWED)


class ReservationDetails(APIView):
    """
    shows details of specific reservation, edits or deletes it
    """

    def get(self, request, pk, pk2):
        reservation = get_object_or_404(Reservation, pk=pk2)
        serializer = ReservationWithDetailsSerializer(reservation, many=False)
        return Response(serializer.data)

    def put(self, request, pk, pk2):
        car = get_object_or_404(Car, pk=pk)
        reservation = get_object_or_404(Reservation, pk=pk2)
        serializer = MiniReservationSerializer(reservation, data=request.data)

        if Reservation.is_period_valid(car, request.data['date_from'], request.data['date_to']):
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(Reservation.get_reason_of_error(), status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def patch(self, request, pk, pk2):
        car = get_object_or_404(Car, pk=pk)
        reservation = get_object_or_404(Reservation, pk=pk2)
        serializer = MiniReservationSerializer(reservation, data=request.data, partial=True)

        new_from = request.data['date_from'] if 'date_from' in list(request.data.keys()) else reservation.date_from
        new_to = request.data['date_to'] if 'date_to' in list(request.data.keys()) else reservation.date_to

        if Reservation.is_period_valid(car, new_from, new_to, reservation):
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(Reservation.get_reason_of_error(), status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def delete(self, request, pk, pk2):
        reservation = get_object_or_404(Reservation, pk=pk2)
        reservation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
