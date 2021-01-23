from rest_framework import serializers

from data_base_course_work_backend.flight_app.models import Employee, Company


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ('name', 'second_name', 'company', 'position')

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('name', 'type')