# Create your views here.
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from .db_utils import get_buisiness_class, book_tickets, get_tickets_price

@api_view(['POST'])
def get_business(request: Request) -> Response:
    flight_id = request.data.get('id')
    data = get_buisiness_class(flight_id)
    return Response(data, status=status.HTTP_200_OK)

@api_view(['POST'])
def book_ticket(request: Request) -> Response:
    contact_info = request.data.get('contact')
    passengers = request.data.get('passengers')
    flight_id = request.data.get('flight')
    
    booking_id = book_tickets(contact_info, passengers, flight_id)
    return Response(booking_id, status=status.HTTP_200_OK)

@api_view(['POST'])
def get_price(request: Request) -> Response:

    passengers = request.data.get('passengers')
    flight_id = request.data.get('flight')
    
    amount = get_tickets_price(passengers, flight_id)
    
    return Response(amount, status=status.HTTP_200_OK)
