from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from data_base_course_work_backend.booking.models import Passenger
from data_base_course_work_backend.booking.serializer import PassengerSerializer, BaggageSerializer
from data_base_course_work_backend.flight_app.models import Flight, Baggage


@api_view(['POST'])
def book_ticket(request: Request) -> Response:
    contact_info = request.data.get('contact')
    passengers = request.data.get('passengers')
    flight = request.data.get('flight')
    count_tickets = request.data.get('count')
    print(passengers)
    flight = Flight.objects.get(id=flight)
    for passenger in passengers:
        passenger_serializer = PassengerSerializer(passenger)
        passenger = Passenger.objects.get(passport_no=passenger_serializer.data.get('passport_no'))
            # Passenger.objects.create(passport_no=passenger_serializer.data.get('passport_no'),
            #                          name=passenger_serializer.data.get('name'), second_name=passenger_serializer.data.get('second_name'),
            #                             third_name=passenger_serializer.data.get('third_name'),
            #                             birthday=passenger_serializer.data.get('birthday'))
            #

        baggage = Baggage()
        print(passenger.name)

    return Response('cool')
