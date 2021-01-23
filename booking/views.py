from django.db import connection
from django.db.models import Q
from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from data_base_course_work_backend.booking.models import Passenger
from data_base_course_work_backend.booking.serializer import PassengerSerializer, BaggageSerializer
from data_base_course_work_backend.flight_app.models import Flight, Baggage, Ticket, Seat

def calculate_price(max_weight, relaxing_room, seat_no, flight_id) -> float:
    cursor = connection.cursor()
    cursor.execute(f'select calc_ticket_price({flight_id}, \'{seat_no}\');')
    row = cursor.fetchall()
    row = row[0][0]
    print(row)
    rel_room_c = {
        'middle': 200,
        'comfort': 500,
        'comfort+': 1000,
    }
    row += rel_room_c[relaxing_room]
    baggage_c = 200
    row += max_weight * baggage_c
    return row



@api_view(['POST'])
def get_business(request: Request) -> Response:
    flight_id = request.data.get('id')
    tickets = Ticket.objects.all()
    tickets_id = [i.seat_id for i in tickets]
    seats = Seat.objects.filter(~Q(id__in=tickets_id), flight_id=flight_id, class_field='business').count()
    data = {
        'seats': seats
    }
    return Response(data, status=status.HTTP_200_OK)

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

@api_view(['POST'])
def get_price(request: Request) -> Response:
    passengers = request.data.get('passengers')
    flight_id = request.data.get('flight')
    tickets = Ticket.objects.all()
    tickets_id = [i.seat_id for i in tickets]
    print(tickets_id)
    seats = Seat.objects.filter(~Q(id__in=tickets_id), flight_id=flight_id)
    print(seats)
    seats_classes = {
        'economy': seats.filter(class_field='economy').first(),
        'business': seats.filter(class_field='business').first()
    }
    amount = 0
    for passenger in passengers:
        seat_type = passenger['seat']
        has_baggage = True if int(passenger['max_weight']) != 0 else False
        relaxing_room_type = passenger['waitingRoom']
        print(seats_classes[seat_type])
        amount += calculate_price(passenger['max_weight'], relaxing_room_type, seats_classes[seat_type].number, flight_id)
        passenger_serializer = PassengerSerializer(passenger)
        passenger = Passenger.objects.get(passport_no=passenger_serializer.data.get('passport_no'))
        print(passenger)

    # cursor = connection.cursor()
    # cursor.execute("select calc_ticket_price(1, 'A21');")
    # row = cursor.fetchall()
    # print(row)
    return Response(amount, status=status.HTTP_200_OK)
