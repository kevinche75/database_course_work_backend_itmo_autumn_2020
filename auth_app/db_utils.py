from flight_app.models import Employee
from flight_app.models import GateSchedule, ReceptionSchedule, Ticket, Baggage, Passenger
from rest_framework import status


def get_employee_from_db(passport_id: str) -> Employee:
    try:
        employee = Employee.objects.get(passport_no=passport_id)
        print(employee)
        return employee
    except Employee.DoesNotExist:
        return None

def get_schedule(employee):

    position = employee.position
    if position == 'gate':
        schedule = GateSchedule.objects.filter(employee_id=employee.passport_no)
    else:
        schedule = ReceptionSchedule.objects.filter(employee_id=employee.passport_no)

    return schedule

def get_current_schedule(employee):

    schedule = get_schedule(employee)

    data = {}

    for i, sch in enumerate(schedule):
        sch_data = {
            'flight': sch.flight_id,
            'gate': sch.gate_number if employee.position == 'gate' else sch.reception_number,
            'start': sch.start_time,
            'finish': sch.finish_time
        }
        data[i] = sch_data

    return data

def get_passenger_info(passport_no, flight_id):

    try:
        passenger = Passenger.objects.get(passport_no=passport_no)
    except Passenger.DoesNotExist:
        return None
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

    return data

def register_passenger(passport_no, flight_id, total_weight):

    try:
        passenger = Passenger.objects.get(passport_no=passport_no)
    except Passenger.DoesNotExist:
        return False
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

    return True

def set_passenger_land(passport_no, flight_id, baggage_status):

    try:
        passenger = Passenger.objects.get(passport_no=passport_no)
    except Passenger.DoesNotExist:
        return status.HTTP_409_CONFLICT
    ticket = Ticket.objects.get(passenger_id=passport_no, seat__flight_id=flight_id)
    if not ticket.registered:
        return status.HTTP_401_UNAUTHORIZED
    try:
        baggage = Baggage.objects.get(ticket_id=ticket.id)
        baggage.status = baggage_status
        baggage.save()
    except Baggage.DoesNotExist:
       pass

    return status.HTTP_200_OK