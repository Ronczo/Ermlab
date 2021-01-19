from django.db import models


class Car(models.Model):
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    registration_number = models.CharField(max_length=15, unique=True)
    date_of_next_technical_examination = models.DateField()

    def __str__(self):
        return f"{self.brand} - {self.model} - {self.registration_number}"


class Reservation(models.Model):
    reservating_person = models.CharField(max_length=40)
    reservation_date_from = models.DateTimeField()
    reservation_date_to = models.DateTimeField()
    booked_car = models.ForeignKey(Car, on_delete=models.PROTECT)

    def __str__(self):
        return f"Reservation from {self.reservation_date_from} to {self.reservation_date_to} for car {self.booked_car}"