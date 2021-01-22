from .models import Employee

def get_employee_from_db(passport_id: int) -> Employee:
    employee = Employee.objects.get(passport_no=passport_id)
    return employee

