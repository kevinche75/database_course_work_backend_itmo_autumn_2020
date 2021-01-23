from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response


@api_view(['POST'])
def book_ticket(request: Request) -> Response:
    contact_info = request.data.get('contact')
    passengers = request.data.get('passengers')
    flight = request.data.get('flight')
