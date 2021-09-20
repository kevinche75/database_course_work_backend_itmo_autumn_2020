from datetime import datetime

from django.db import connection
from django.db.models import Q
from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from booking.models import Passenger
from booking.serializer import PassengerSerializer, BaggageSerializer
from flight_app.models import Flight, Baggage, Ticket, Seat, Booking, RelaxRoomBooking


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
    flight_id = request.data.get('flight')

    tickets = Ticket.objects.all()
    tickets_id = [i.seat_id for i in tickets]
    seats = Seat.objects.filter(~Q(id__in=tickets_id), flight_id=flight_id)
    seats_classes = {
        'economy': seats.filter(class_field='economy').values('number','id'),
        'business': seats.filter(class_field='business').values('number', 'id')
    }
    amount = 0
    passengers_id = []
    seat_tickets = []
    for passenger in passengers:
        seat = list(seats_classes[passenger['seat']]).pop()
        relaxing_room_type = passenger['waitingRoom']
        max_weight = passenger['max_weight']
        seat_price = calculate_price(max_weight, relaxing_room_type, seat['number'], flight_id)
        amount += seat_price
        seat_tickets.append((seat['id'], seat_price))
        passenger_serializer = PassengerSerializer(passenger)
        passenger = Passenger.objects.get_or_create(passport_no=passenger_serializer.data.get('passport_no'),
                                                    name=passenger_serializer.data.get('second_name'),
                                                    second_name=passenger_serializer.data.get('name'),
                                                    third_name=passenger_serializer.data.get('third_name'),
                                                    birthday=str(passenger_serializer.data.get('birthday'))[:10])[0]
        passengers_id.append(passenger.pk)
    cursor = connection.cursor()
    cursor.execute(f'select to_book_trip(\'{contact_info}\', {amount});')
    booking_id = cursor.fetchall()[0][0]
    print(booking_id)
    for i, passenger in enumerate(passengers):
        max_weight = passenger['max_weight']
        ticket = Ticket.objects.create(passenger_id=passengers_id[i],
                                       seat_id=seat_tickets[i][0],
                                       amount=seat_tickets[i][1],
                                       book_id=booking_id,
                                       registered=False)
        if max_weight != 0:
            baggage = Baggage.objects.create(ticket_id=ticket.pk,
                                             max_weight=max_weight,
                                             status='offered')
        relax_room_booking = RelaxRoomBooking.objects.create(ticket_id=ticket.pk, class_field=passenger['waitingRoom'])
    return Response(booking_id, status=status.HTTP_200_OK)

@api_view(['POST'])
def get_price(request: Request) -> Response:
    passengers = request.data.get('passengers')
    flight_id = request.data.get('flight')
    tickets = Ticket.objects.all()
    tickets_id = [i.seat_id for i in tickets]
    seats = Seat.objects.filter(~Q(id__in=tickets_id), flight_id=flight_id)
    seats_classes = {
        'economy': seats.filter(class_field='economy').first(),
        'business': seats.filter(class_field='business').first()
    }
    amount = 0
    for passenger in passengers:
        seat_type = passenger['seat']
        relaxing_room_type = passenger['waitingRoom']
        print(seats_classes[seat_type])
        amount += calculate_price(passenger['max_weight'], relaxing_room_type, seats_classes[seat_type].number, flight_id)
        # passenger_serializer = PassengerSerializer(passenger)
        # passenger = Passenger.objects.get(passport_no=passenger_serializer.data.get('passport_no'))
        # print(passenger)

    # cursor = connection.cursor()
    # cursor.execute("select calc_ticket_price(1, 'A21');")
    # row = cursor.fetchall()
    # print(row)
    return Response(amount, status=status.HTTP_200_OK)
