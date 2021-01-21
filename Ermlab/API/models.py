from django.db import models
from datetime import datetime


class Car(models.Model):
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    registration_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
    date_of_next_technical_examination = models.DateField()

    def __str__(self):
        return f"{self.brand} - {self.model} - {self.registration_number}"


class Reservation(models.Model):
    booking_person = models.CharField(max_length=40)
    date_from = models.DateTimeField()
    date_to = models.DateTimeField()
    booked_car = models.ForeignKey(Car, on_delete=models.PROTECT)

    def __str__(self):
        return f"Reservation from {self.date_from} to {self.date_to} for car {self.booked_car}"

    @staticmethod
    def get_reservations(car):
        """
        :param car: should be an object of class Car
        :return: Returns list of reservations of the specific car
        """

        return [reservation for reservation in Reservation.objects.filter(booked_car=car)]

    @staticmethod
    def is_period_valid(choosed_car, new_from, new_to):
        """
        The method checks if new reservation date dosen't collide with existing ones
        :param choosed_car: should be an object of class Car
        :param new_from: this is date when new reservation starts
        :param new_to: this is date when new reservation ends
        """

        # Creates a list of tuples with dates of reservations
        dates_of_reservations = []
        for reservation in Reservation.get_reservations(choosed_car):
            dates_of_reservations.append((reservation.date_from, reservation.date_to))

        # Converts string into datetime object
        new_from = datetime.strptime(new_from, '%Y-%m-%dT%H:%M:%S%z') if not isinstance(new_from, datetime) else new_from
        new_to = datetime.strptime(new_to, '%Y-%m-%dT%H:%M:%S%z') if not isinstance(new_to, datetime) else new_to

        if choosed_car.date_of_next_technical_examination >= new_to.date():
            if new_from <= new_to:
                if dates_of_reservations:
                    for reservation in dates_of_reservations:
                        if any(map(lambda x: reservation[0] <= x <= reservation[1], (new_from, new_to))):
                            return False
                    return True
                else:
                    return True
            else:
                return False
        else:
            return False
