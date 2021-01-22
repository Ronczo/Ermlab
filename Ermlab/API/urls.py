from django.urls import path
from . import views

urlpatterns = [
    path('cars', views.CarList.as_view()),
    path('car/<int:pk>', views.CarDetail.as_view()),
    path('car/<int:pk>/reservations', views.ReservationList.as_view()),
    path('car/<int:pk>/reservations/<int:pk2>', views.ReservationDetails.as_view()),
]
