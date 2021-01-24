from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from data_base_course_work_backend.flight_app.models import Aircraft, Company, Flight, Employee, GateSchedule, \
    ReceptionSchedule


@api_view(['GET'])
def get_aircrafts(request: Request) -> Response:
    data = {}
    aircrafts = Aircraft.objects.all()
    for i, aircraft in enumerate(aircrafts):
        aircraft = {
           'company': aircraft.owner_id,
           'id': aircraft.id,
           'location': aircraft.location,
           'aircraftmodel': aircraft.model
        }
        data[i] = aircraft

    return Response(data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_companies(request: Request) -> Response:
    data = {}
    companies = Company.objects.all()
    for i, company in enumerate(companies):
        company = {
           'name': company.type,
           'type': company.name,
        }
        data[i] = company

    return Response(data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_flights(request: Request) -> Response:
    data = {}
    flights = Flight.objects.all()
    for i, flight in enumerate(flights):
        flight = {
            'id': flight.id,
            'dep': flight.departure_airport,
            'arr': flight.arrival_airport,
            'deptime': flight.schedule_departure,
            'arrtime': flight.schedule_arrival,
            'count': 1,
            'actualArrtime': flight.actual_arrival,
            'actualDeptime': flight.actual_departure,
            'aircraft': flight.aircraft.id,
            'status': flight.status,
        }
        data[i] = flight

    return Response(data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_schedule(request: Request, passport) -> Response:
    data = {}
    print(passport)
    employee_position = Employee.objects.get(passport_no=passport).position
    if employee_position == 'gate':
        schedule = GateSchedule.objects.filter(employee_id=passport)
    elif employee_position == 'reception':
        schedule = ReceptionSchedule.objects.filter(employee_id=passport)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)
    for i, schedule_row in enumerate(schedule):
        schedule_row = {
            'flight': schedule_row.flight_id,
            'gate': schedule_row.gate_number if employee_position == 'gate' else schedule_row.reception_number,
            'start': schedule_row.start_time,
            'finish': schedule_row.finish_time,
        }
        data[i] = schedule_row

    return Response(data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_employee(request: Request) -> Response:
    data = {}
    employees = Employee.objects.filter(position__in=['reception', 'gate'])
    for i, employee in enumerate(employees):
        employee = {
            'passport': employee.passport_no,
            'name': employee.second_name,
            'surname': employee.name,
            'pathronymic': employee.third_name,
            'company': employee.company.name,
            'position': employee.position,
        }
        data[i] = employee

    return Response(data, status=status.HTTP_200_OK)

@api_view(['POST'])
def add_aircraft(request: Request) -> Response:
    aircraft_id = request.data.get('id')
    model = request.data.get('model')
    company = request.data.get('company')
    Aircraft.objects.create(id=aircraft_id, owner_id=company, model=model)
    return Response(status=status.HTTP_200_OK)

@api_view(['POST'])
def add_employee(request: Request) -> Response:
    passport_no = request.data.get('passport')
    name = request.data.get('name')
    second_name = request.data.get('surname')
    third_name = request.data.get('pathronymic')
    position = request.data.get('position')
    company = request.data.get('company')
    try:
        Company.objects.get(name=company)
    except Company.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    employee, created = Employee.objects.get_or_create(passport_no=passport_no, name=second_name, second_name=name,
                                    third_name=third_name, position=position,
                                    company_id=company)
    if not created:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    return Response(status=status.HTTP_200_OK)

@api_view(['POST'])
def add_flight(request: Request) -> Response:
    aircraft_id = request.data.get('aircraft_id')
    schedule_departure = request.data.get('schedule_departure')
    schedule_arrival = request.data.get('schedule_arrival')
    departure_airport = request.data.get('departure_airport')
    arrival_airport = request.data.get('arrival_airport')
    flight, created = Flight.objects.get_or_create(aircraft_id=aircraft_id, schedule_departure=schedule_departure,
                                                   schedule_arrival=schedule_arrival,
                                                   departure_airport=departure_airport,
                                                   arrival_airport=arrival_airport,
                                                   status='scheduled')
    if not created:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    return Response(status=status.HTTP_200_OK)

@api_view(['POST'])
def add_schedule(request: Request) -> Response:
    employee_id = request.data.get('employee_id')
    flight_id = request.data.get('flight_id')
    start_time = request.data.get('start_time')
    finish_time = request.data.get('finish_time')
    gate = request.data.get('gate')
    employee_position = Employee.objects.get(passport_no=employee_id).position
    if employee_position == 'gate':
        gate, created = GateSchedule.objects.get_or_create(employee_id=employee_id, flight_id=flight_id, gate_number=gate,
                                           start_time=start_time, finish_time=finish_time)
    elif employee_position == 'reception':
        reception, created = ReceptionSchedule.objects.get_or_create(employee_id=employee_id, flight_id=flight_id, reception_number=gate,
                                           start_time=start_time, finish_time=finish_time)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if not created:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_200_OK)

@api_view(['POST'])
def add_company(request: Request) -> Response:
    name = request.data.get('name')
    type_c = request.data.get('type')
    company, created = Company.objects.get_or_create(name=name, type=type_c)
    if not created:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_200_OK)

@api_view(['POST'])
def delete_aircraft(request: Request) -> Response:
    aircraft_id = request.data.get('id')
    Aircraft.objects.get(id=aircraft_id).delete()
    return Response(f'{aircraft_id} aircraft was deleted', status=status.HTTP_200_OK)

@api_view(['POST'])
def change_aircraft(request: Request) -> Response:
    owner_id = request.data.get('owner_id')
    aircraft_id = request.data.get('id')
    model = request.data.get('model')
    aircraft = Aircraft.objects.get(id=aircraft_id)
    aircraft.owner_id = owner_id
    aircraft.model = model
    aircraft.save()
    return Response(status=status.HTTP_200_OK)

@api_view(['POST'])
def delete_company(request: Request) -> Response:
    company_name = request.data.get('name')
    Company.objects.get(name=company_name).delete()
    return Response(f'{company_name} company was deleted', status=status.HTTP_200_OK)

@api_view(['POST'])
def delete_employee(request: Request) -> Response:
    passport_no = request.data.get('passport')
    Employee.objects.get(passport_no=passport_no).delete()
    return Response(f'{passport_no} employee was deleted', status=status.HTTP_200_OK)


@api_view(['POST'])
def change_employee(request: Request) -> Response:
    employee = request.data.get('employee')
    emp_dp = Employee.objects.get(passport_no=employee['passport'])
    emp_dp.second_name = employee['name']
    emp_dp.name = employee['surname']
    emp_dp.third_name = employee['pathronymic']
    emp_dp.company.name = employee['company']
    emp_dp.position = employee['position']
    emp_dp.save()
    return Response(status=status.HTTP_200_OK)

@api_view(['POST'])
def delete_flight(request: Request) -> Response:
    flight_id = request.data.get('id')
    Flight.objects.get(id=flight_id).delete()
    return Response(f'{flight_id} flight was deleted', status=status.HTTP_200_OK)

@api_view(['POST'])
def change_flight(request: Request) -> Response:
    flight = request.data.get('flight')
    print(flight)
    flight_db = Flight.objects.get(id=flight['id'])
    flight_db.aircraft.id = flight['aircraft']
    flight_db.schedule_arrival = flight['arrtime']
    flight_db.schedule_departure = flight['deptime']
    flight_db.actual_departure = flight['actualDeptime']
    flight_db.actual_arrival = flight['actualArrtime']
    flight_db.status = flight['status']
    flight_db.departure_airport = flight['dep']
    flight_db.arrival_airport = flight['arr']
    flight_db.save()
    return Response(status=status.HTTP_200_OK)

@api_view(['POST'])
def delete_work(request: Request) -> Response:
    flight_id = request.data.get('flight')
    employee_id = request.data.get('employee')
    employee_position = Employee.objects.get(passport_no=employee_id).position
    if employee_position == 'gate':
        GateSchedule.objects.get(employee_id=employee_id, flight_id=flight_id).delete()
    elif employee_position == 'reception':
        ReceptionSchedule.objects.get(employee_id=employee_id, flight_id=flight_id).delete()
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_200_OK)

@api_view(['POST'])
def change_work(request: Request) -> Response:
    schedule = request.data.get('work')
    employee_id = request.data.get('employee')
    employee_position = Employee.objects.get(passport_no=employee_id).position
    if employee_position == 'gate':
        schedule_db = GateSchedule.objects.get(employee_id=employee_id, flight_id=schedule['flight'])
        schedule_db.gate_number = schedule['gate']
        schedule_db.start_time = schedule['start']
        schedule_db.finish_time = schedule['finish']
        schedule_db.save()
    elif employee_position == 'reception':
        schedule_db = ReceptionSchedule.objects.get(employee_id=employee_id, flight_id=schedule['flight'])
        schedule_db.reception_number = schedule['gate']
        schedule_db.start_time = schedule['start']
        schedule_db.finish_time = schedule['finish']
        schedule_db.save()
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_200_OK)



