from django.urls import path
#from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('cars/', views.CarList.as_view()),
    path('car/<int:pk>', views.CarDetail.as_view()),
    path('car/<int:pk>/reservations', views.ReservationList.as_view()),
    path('car/<int:pk>/reservations/<int:pk2>', views.ReservationDetails.as_view()),
]

#urlpatterns = format_suffix_patterns(urlpatterns)
