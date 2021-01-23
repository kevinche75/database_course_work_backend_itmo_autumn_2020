from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from django.db.models import Q, Count
from datetime import datetime
from data_base_course_work_backend.flight_app.models import TripPrice, Flight, Ticket, Seat


@api_view(['GET'])
def search_direction(request: Request) -> Response:
    trips = TripPrice.objects.all()
    directions = set()
    for i in trips:
        directions.add(i.arrival_airport)
        directions.add(i.departure_airport)
    return Response(directions, status=status.HTTP_200_OK)

@api_view(['POST'])
def get_flights(request: Request) -> Response:
    arrival_airport = request.data.get('arr')
    departure_airport = request.data.get('dep')
    flight_date = str(request.data.get('date'))[:10]
    count_seat = request.data.get('count')
    flights = Flight.objects.filter(departure_airport=departure_airport,
                                    arrival_airport=arrival_airport)
    flights_id = []
    tickets = Ticket.objects.all()
    tickets_id = [i.seat_id for i in tickets]
    data = {}
    for i in flights.all():

        if flight_date == str(i.schedule_departure)[:10]:
            seats = Seat.objects.filter(~Q(id__in=tickets_id), flight_id=i.id).count()
            if seats >= count_seat:
                flight = {
                    'aircraft': i.aircraft.id,
                    'actualDeptime': i.actual_departure,
                    'actualArrtime': i.actual_arrival,
                    'status': i.status,
                    'id': i.id,
                    'dep': i.departure_airport,
                    'arr': i.arrival_airport,
                    'deptime': i.schedule_departure,
                    'arrtime': i.schedule_arrival,
                    'count': seats
                }
                flights_id.append(i.id)
                data[i.id] = flight
    return Response(data, status=status.HTTP_200_OK)
