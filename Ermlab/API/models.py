from django.db import models

class Car(models.Model):
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    registration_number = models.CharField(max_length=15)
    date_of_next_technical_examination = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.brand} - {self.model} - {self.registration_number}"