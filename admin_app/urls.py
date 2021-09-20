from django.urls import path

from admin_app.views import *

urlpatterns = [
    path('aircraft/get/', get_aircrafts),
    path('aircraft/add/', add_aircraft),
    path('aircraft/delete/', delete_aircraft),
    path('aircraft/change/', change_aircraft),

    path('employee/get/', get_employee),
    path('employee/add/', add_employee),
    path('employee/change/', change_employee),
    path('employee/delete/', delete_employee),


    path('companies/get/', get_companies),
    path('companies/add/', add_company),
    path('companies/delete/', delete_company),

    path('flight/get/', get_flights),
    path('flight/add/', add_flight),
    path('flight/change/', change_flight),
    path('flight/delete/', delete_flight),

    path('schedule/get/<int:passport>', get_schedule),
    path('schedule/add/', add_schedule),
    path('schedule/change/', change_work),
    path('schedule/delete/', delete_work),
]