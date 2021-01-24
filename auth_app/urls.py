from django.urls import path
from .views import auth, get_schedule, get_passenger, registrate_passenger, passenger_to_land

urlpatterns = [
    path('', auth),
    path('schedule/', get_schedule),
    path('passenger/', get_passenger),
    path('passenger/registrate/', registrate_passenger),
    path('passenger/land/', passenger_to_land)
]