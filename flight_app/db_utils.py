from flight_app.models import TripPrice, Flight, Ticket, Seat
from django.db.models import Q, Count


def get_all_directions():
    trips = TripPrice.objects.all()
    directions = set()
    for i in trips:
        directions.add(i.arrival_airport)
        directions.add(i.departure_airport)
    return directions

def flight_converter(i, seats):
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
    return flight

def get_all_available_tickets(departure_airport, arrival_airport, flight_date, count_seat):

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
                flight = flight_converter(i, seats)
                flights_id.append(i.id)
                data[i.id] = flight

    return data