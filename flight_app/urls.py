from django.urls import path

from data_base_course_work_backend.flight_app.views import *

urlpatterns = [
    path('search/direction/', search_direction),
    path('get/', get_flights)
]