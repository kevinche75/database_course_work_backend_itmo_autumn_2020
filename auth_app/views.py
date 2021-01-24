# Create your views here.
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.renderers import JSONRenderer
from rest_framework.request import Request
from rest_framework.response import Response

from . import db_utils


from .serializer import EmployeeSerializer
from jwt_app import jwt_utils

from data_base_course_work_backend.flight_app.models import GateSchedule, ReceptionSchedule, Ticket, Baggage
from data_base_course_work_backend.booking.models import Passenger
from data_base_course_work_backend.booking.serializer import PassengerSerializer


@api_view(['POST'])
def auth(request: Request) -> Response:
    passport_id = request.data.get('passport')
    print(passport_id)
    employee = db_utils.get_employee_from_db(passport_id)
    print(employee)
    position = employee.position if employee is not None else 'null'
    headers = {
        'Access-Token': jwt_utils.generate_access_token(employee.passport_no)
    }
    print(position)

    return Response(position, headers=headers, status=status.HTTP_200_OK)

@api_view(['POST'])
def get_schedule(request: Request) -> Response:
    passport_no = request.data.get('passport')
    employee = db_utils.get_employee_from_db(passport_no)
    position = employee.position
    if position == 'gate':
        schedule = GateSchedule.objects.filter(employee_id=passport_no)
    else:
        schedule = ReceptionSchedule.objects.filter(employee_id=passport_no)

    data = {}

    for i, sch in enumerate(schedule):
        sch_data = {
            'flight': sch.flight_id,
            'gate': sch.gate_number if position == 'gate' else sch.reception_number,
            'start': sch.start_time,
            'finish': sch.finish_time
        }
        data[i] = sch_data

    return Response(data, status=status.HTTP_200_OK)

@api_view(['POST'])
def get_passenger(request: Request) -> Response:
    flight_id = request.data.get('flightID')
    passport_no = request.data.get('passport')
    try:
        passenger = Passenger.objects.get(passport_no=passport_no)
    except Passenger.DoesNotExist:
        return Response(status=status.HTTP_409_CONFLICT)
    ticket = Ticket.objects.get(passenger_id=passport_no, seat__flight_id=flight_id)
    try:
        baggage = Baggage.objects.get(ticket_id=ticket.id)
        baggage_status = baggage.status
        max_weight = baggage.max_weight
    except Baggage.DoesNotExist:
        baggage_status = 'null'
        max_weight = 0
    data = {
        'passport_no': passenger.passport_no,
        'max_weight': max_weight,
        'status': baggage_status
    }

    return Response(data, status=status.HTTP_200_OK)


@api_view(['POST'])
def registrate_passenger(request: Request) -> Response:
    passport_no = request.data.get('passport')
    total_weight = request.data.get('totalWeight')
    flight_id = request.data.get('flightID')
    try:
        passenger = Passenger.objects.get(passport_no=passport_no)
    except Passenger.DoesNotExist:
        return Response(status=status.HTTP_409_CONFLICT)
    ticket = Ticket.objects.get(passenger_id=passport_no, seat__flight_id=flight_id)
    ticket.registered = True
    ticket.save()

    try:
        baggage = Baggage.objects.get(ticket_id=ticket.id)
        baggage.total_weight = total_weight
        baggage.status = 'accept'
        baggage.save()
    except Baggage.DoesNotExist:
        pass

    return Response('registered', status=status.HTTP_200_OK)

@api_view(['POST'])
def passenger_to_land(request: Request) -> Response:
    passport_no = request.data.get('passport')
    flight_id = request.data.get('flightID')
    baggage_status = request.data.get('baggageStatus')
    try:
        passenger = Passenger.objects.get(passport_no=passport_no)
    except Passenger.DoesNotExist:
        return Response(status=status.HTTP_409_CONFLICT)
    ticket = Ticket.objects.get(passenger_id=passport_no, seat__flight_id=flight_id)
    if not ticket.registered:
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    try:
        baggage = Baggage.objects.get(ticket_id=ticket.id)
        baggage.status = baggage_status
        baggage.save()
    except Baggage.DoesNotExist:
       pass

    return Response('Good trip', status=status.HTTP_200_OK)


