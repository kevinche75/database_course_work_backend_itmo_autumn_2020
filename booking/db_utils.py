from django.db import connection
from flight_app.models import Baggage, Ticket, Seat, RelaxRoomBooking
from django.db.models import Q
from booking.models import Passenger
from booking.serializer import PassengerSerializer

MIDDLE_TAX = 200
COMFORT_TAX = 500
COMFORT_PLUS_TAX = 1000
BAGGAGE_TAX = 200

def calculate_price(max_weight, relaxing_room, seat_no, flight_id) -> float:
    cursor = connection.cursor()
    cursor.execute(f'select calc_ticket_price({flight_id}, \'{seat_no}\');')
    row = cursor.fetchall()
    row = row[0][0]
    print(row)
    rel_room_c = {
        'middle': MIDDLE_TAX,
        'comfort': COMFORT_TAX,
        'comfort+': COMFORT_PLUS_TAX,
    }
    row += rel_room_c[relaxing_room]
    row += max_weight * BAGGAGE_TAX
    return row

def get_buisiness_class(flight_id):
    tickets = Ticket.objects.all()
    tickets_id = [i.seat_id for i in tickets]
    seats = Seat.objects.filter(~Q(id__in=tickets_id), flight_id=flight_id, class_field='business').count()
    data = {
        'seats': seats
    }
    return data

def get_classes_tickets(flight_id):
    tickets = Ticket.objects.all()
    tickets_id = [i.seat_id for i in tickets]
    seats = Seat.objects.filter(~Q(id__in=tickets_id), flight_id=flight_id)
    seats_classes = {
        'economy': seats.filter(class_field='economy').values('number','id'),
        'business': seats.filter(class_field='business').values('number', 'id')
    }
    return seats_classes

def find_or_create_passengers(passengers, seats_classes, flight_id):
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

    return amount, passengers_id, seat_tickets

def book_tickets(contact_info, passengers, flight_id):

    seats_classes = get_classes_tickets(flight_id)
    amount, passengers_id, seat_tickets = find_or_create_passengers(passengers, seats_classes, flight_id)

    cursor = connection.cursor()
    cursor.execute(f'select to_book_trip(\'{contact_info}\', {amount});')
    booking_id = cursor.fetchall()[0][0]

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

    return booking_id

def get_tickets_price(passengers, flight_id):

    seats_classes = get_classes_tickets(flight_id)

    amount = 0
    for passenger in passengers:
        seat_type = passenger['seat']
        relaxing_room_type = passenger['waitingRoom']
        amount += calculate_price(passenger['max_weight'], relaxing_room_type, seats_classes[seat_type].number, flight_id)

    return amount