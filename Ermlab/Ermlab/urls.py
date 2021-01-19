from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from API.views import CarViewSet

router = routers.DefaultRouter()
router.register(r'cars', CarViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('API.urls')),
    path('', include(router.urls))
]
