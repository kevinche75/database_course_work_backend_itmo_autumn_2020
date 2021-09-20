# Create your views here.
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from .db_utils import get_all_directions, get_all_available_tickets

@api_view(['GET'])
def search_direction(request: Request) -> Response:
    directions = get_all_directions()
    return Response(directions, status=status.HTTP_200_OK)

@api_view(['POST'])
def get_flights(request: Request) -> Response:

    arrival_airport = request.data.get('arr')
    departure_airport = request.data.get('dep')
    flight_date = str(request.data.get('date'))[:10]
    count_seat = request.data.get('count')

    available_tickets = get_all_available_tickets(departure_airport, arrival_airport, flight_date, count_seat)
    return Response(available_tickets, status=status.HTTP_200_OK)
