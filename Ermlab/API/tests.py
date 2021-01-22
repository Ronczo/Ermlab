from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Car, Reservation


class CarListTest(APITestCase):

    def test_car_list(self):
        response = self.client.get('/api/cars')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class CarDetailsTest(APITestCase):

    def setUp(self):
        Car.objects.create(brand='Opel', model="Astra", registration_number="NO9580",
                           date_of_next_technical_examination="2021-03-19")

    def test_get_car(self):
        response = self.client.get("/api/car/1")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_car(self):
        data = {
            "brand": "Toyota",
            "model": "Avensis",
            "registration_number": "NO7845",
            "date_of_next_technical_examination": "2022-01-04"
        }
        response = self.client.post("/api/car/1", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_put_car(self):
        data = {
            "brand": "Skoda",
            "model": "Octavia",
            "registration_number": "NOL17845",
            "date_of_next_technical_examination": "2022-03-04"
        }
        response = self.client.put("/api/car/1", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patch_car(self):
        data = {
            "brand": "BMW",
            "model": "x7",
        }
        response = self.client.patch("/api/car/1", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_car_without_reservation(self):
        response = self.client.delete("/api/car/1")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_car_with_reservation(self):
        Reservation.objects.create(booking_person="Marcin", date_from="2021-01-10T03:00:00Z",
                                   date_to="2021-01-20T00:00:00Z", booked_car=Car.objects.filter(pk=1)[0])
        response = self.client.delete("/api/car/1")
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class ReservationListTest(APITestCase):

    def setUp(self):
        Car.objects.create(brand='Opel', model="Astra", registration_number="NO9580",
                           date_of_next_technical_examination="2021-03-19")
        Reservation.objects.create(booking_person="Marcin", date_from="2021-01-10T03:00:00Z",
                                   date_to="2021-01-20T00:00:00Z", booked_car=Car.objects.filter(pk=1)[0])

    def test_get_reservations(self):
        response = self.client.get("/api/car/1/reservations")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_reservation(self):
        """
        tests putting reservation without collision with another reservation
        """
        data = {
            'booking_person': "Ewelina",
            'date_from': "2021-01-21T03:00:00Z",
            'date_to': "2021-01-23T00:00:00Z"
        }
        response = self.client.post("/api/car/1/reservations", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_reservation_with_collision(self):
        """
        tests putting reservation with collision with another reservation
        """
        data = {
            'booking_person': "Ewelina",
            'date_from': "2021-01-11T03:00:00Z",
            'date_to': "2021-01-23T00:00:00Z"
        }
        response = self.client.post("/api/car/1/reservations", data)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_post_reservation_with_wrong_dates(self):
        """
        tests putting reservation if date_from is later than date_to
        """
        data = {
            'booking_person': "Ewelina",
            'date_from': "2021-01-24T03:00:00Z",
            'date_to': "2021-01-23T00:00:00Z"
        }
        response = self.client.post("/api/car/1/reservations", data)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_post_reservation_with_exceeded_examination(self):
        """
        tests putting reservation if reservation ends after planned car's technical examination
        """
        data = {
            'booking_person': "Ewelina",
            'date_from': "2021-02-24T03:00:00Z",
            'date_to': "2021-03-23T00:00:00Z"
        }
        response = self.client.post("/api/car/1/reservations", data)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class ReservationDetailsTest(APITestCase):

    def setUp(self):
        Car.objects.create(brand='Opel', model="Astra", registration_number="NO9580",
                           date_of_next_technical_examination="2021-03-19")
        Reservation.objects.create(booking_person="Marcin", date_from="2021-01-10T03:00:00Z",
                                   date_to="2021-01-20T00:00:00Z", booked_car=Car.objects.filter(pk=1)[0])

    def test_get_reservation(self):
        response = self.client.get("/api/car/1/reservations/1")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put_reservation(self):
        """
        Collisions were tested in ReservationListTest (post method)
        """

        data = {
            "booking_person": "Maciej",
            "date_from": "2021-01-21T03:00:00Z",
            "date_to": "2021-01-22T00:00:00Z",
        }

        response = self.client.put("/api/car/1/reservations/1", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patch_reservation(self):
        data = {
            "booking_person": "Natalia",
            # "date_from": "2021-01-01T03:00:00Z",
            "date_to": "2021-02-01T03:00:00Z",
        }
        response = self.client.patch("/api/car/1/reservations/1", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_reservation(self):
        response = self.client.delete("/api/car/1/reservations/1")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class ReservationMethodTest(TestCase):

    def setUp(self):
        Car.objects.create(brand='Opel', model="Astra", registration_number="NO9580",
                           date_of_next_technical_examination="2021-03-19")
        Reservation.objects.create(booking_person="Marcin", date_from="2021-01-10T03:00:00Z",
                                   date_to="2021-01-20T00:00:00Z", booked_car=Car.objects.filter(pk=1)[0])

    def test_date_to_after_examination(self):
        car = Car.objects.get(brand="Opel")
        new_reservation = Reservation.objects.create(booking_person="Marcin", date_from="2021-01-22T03:00:00Z",
                                                     date_to="2021-04-20T00:00:00Z",
                                                     booked_car=Car.objects.filter(pk=1)[0])
        self.assertEqual(new_reservation.is_period_valid(car, new_reservation.date_from, new_reservation.date_to),
                         False)

    def test_date_to_is_ealier(self):
        car = Car.objects.get(brand="Opel")
        new_reservation = Reservation.objects.create(booking_person="Marcin", date_from="2021-02-22T03:00:00Z",
                                                     date_to="2021-03-18T00:00:00Z",
                                                     booked_car=Car.objects.filter(pk=1)[0])
        self.assertEqual(new_reservation.is_period_valid(car, new_reservation.date_from, new_reservation.date_to),
                         False)

    def test_reservation_collids_with_another(self):
        car = Car.objects.get(brand="Opel")
        new_reservation = Reservation.objects.create(booking_person="Marcin", date_from="2021-01-11T03:00:00Z",
                                                     date_to="2021-01-22T00:00:00Z",
                                                     booked_car=Car.objects.filter(pk=1)[0])
        self.assertEqual(new_reservation.is_period_valid(car, new_reservation.date_from, new_reservation.date_to),
                         False)