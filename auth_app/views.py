# Create your views here.
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from . import db_utils


from jwt_app import jwt_utils


@api_view(['POST'])
def auth(request: Request) -> Response:
    passport_id = request.data.get('passport')

    employee = db_utils.get_employee_from_db(passport_id)
    position = employee.position if employee is not None else 'null'

    headers = {
        'Access-Token': jwt_utils.generate_access_token(employee.passport_no)
    }

    return Response(position, headers=headers, status=status.HTTP_200_OK)

@api_view(['POST'])
def get_schedule(request: Request) -> Response:
    passport_no = request.data.get('passport')
    employee = db_utils.get_employee_from_db(passport_no)
    data = db_utils.get_current_schedule(employee)

    return Response(data, status=status.HTTP_200_OK)

@api_view(['POST'])
def get_passenger(request: Request) -> Response:
    flight_id = request.data.get('flightID')
    passport_no = request.data.get('passport')
    
    data = db_utils.get_passenger_info(passport_no, flight_id)

    if not data:
        return Response(status=status.HTTP_409_CONFLICT)

    return Response(data, status=status.HTTP_200_OK)


@api_view(['POST'])
def registrate_passenger(request: Request) -> Response:
    passport_no = request.data.get('passport')
    total_weight = request.data.get('totalWeight')
    flight_id = request.data.get('flightID')

    registered = db_utils.register_passenger(passport_no, flight_id, total_weight)

    if not registered:
        return Response(status=status.HTTP_409_CONFLICT)

    return Response('registered', status=status.HTTP_200_OK)

@api_view(['POST'])
def passenger_to_land(request: Request) -> Response:
    passport_no = request.data.get('passport')
    flight_id = request.data.get('flightID')
    baggage_status = request.data.get('baggageStatus')
    
    status = db_utils.set_passenger_land(passport_no, flight_id, baggage_status)

    return Response(status=status)


