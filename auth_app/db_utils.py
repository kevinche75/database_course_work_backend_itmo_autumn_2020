from data_base_course_work_backend.flight_app.models import Employee


def get_employee_from_db(passport_id: str) -> Employee:
    try:
        employee = Employee.objects.get(passport_no=passport_id)
        print(employee)
        return employee
    except Employee.DoesNotExist:
        return None

