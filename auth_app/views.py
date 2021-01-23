# Create your views here.
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.renderers import JSONRenderer
from rest_framework.request import Request
from rest_framework.response import Response

from . import db_utils


from .serializer import EmployeeSerializer
from jwt_app import jwt_utils

from data_base_course_work_backend.flight_app.models import GateSchedule, ReceptionSchedule
from ..booking.models import Passenger
from ..booking.serializer import PassengerSerializer


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

def get_passenger(request: Request) -> Response:
    flight_id = request.data.get('flightID')
    passport_no = request.data.get('passport')
    try:
        passenger = Passenger.objects.get(passport_no=passport_no)
    except Passenger.DoesNotExist:
        return Response(status=status.HTTP_409_CONFLICT)
    passenger = PassengerSerializer(passenger)
