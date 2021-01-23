# Create your views here.
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.renderers import JSONRenderer
from rest_framework.request import Request
from rest_framework.response import Response

from . import db_utils
from .serializer import EmployeeSerializer
from jwt_app import jwt_utils


@api_view(['GET'])
def auth(request: Request) -> Response:
    passport_id = request.query_params.get('id')
    employee = db_utils.get_employee_from_db(passport_id)
    employee_serializer = EmployeeSerializer(employee)
    headers = {
        'Access-Token': jwt_utils.generate_access_token(employee.passport_no)
    }
    data = {
        'employee': employee_serializer.data
    }
    return Response(data, headers=headers, status=status.HTTP_200_OK)



