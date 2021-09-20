from django.urls import path

from flight_app.views import *

urlpatterns = [
    path('search/direction/', search_direction),
    path('get/', get_flights)
]