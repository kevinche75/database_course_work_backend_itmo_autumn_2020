from datetime import datetime, timedelta
import jwt
from django.conf import settings


def set_token_to_response_headers(employee_no) -> dict:
    access_token = generate_access_token(employee_no)
    employee_headers = {'Access-Token': access_token}
    return employee_headers


def generate_access_token(employee_no) -> str:

    access_token_payload = {
        'employee_no': employee_no,
        'exp': datetime.utcnow() + timedelta(days=0, minutes=60),
        'iat': datetime.utcnow(),
    }

    access_token = jwt.encode(access_token_payload,
                              settings.SECRET_KEY, algorithm='HS256')
    return access_token

def get_employee_no_from_payload(access_token: str) -> str:
    access_token_payload = jwt.decode(access_token, settings.SECRET_KEY, algorithm='HS256')
    employee_no = access_token_payload.get('employee_no')
    print('employee_no = {}'.format(employee_no))
    return employee_no


def validate_token(token) -> bool:
    if validate_token_signature(token) and validate_token_timeout(token):
        print('token is validate')
        return True
    else:
        print('token is not validate')
        return False


def validate_token_signature(token) -> bool:
    client_payload = jwt.decode(token, settings.SECRET_KEY, algorithm='HS256')
    server_token = jwt.encode(client_payload, settings.SECRET_KEY, algorithm='HS256')
    return True if server_token == token else False

def validate_token_timeout(token) -> bool:
    client_payload = jwt.decode(token, settings.SECRET_KEY, algorithm='HS256')
    exp = client_payload.get('exp')
    iat = client_payload.get('iat')
    return True if exp > iat else False
