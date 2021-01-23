from rest_framework import serializers

from data_base_course_work_backend.booking.models import Passenger
from data_base_course_work_backend.flight_app.models import Baggage


class PassengerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Passenger
        fields = ('passport_no', 'second_name', 'birthday', 'third_name', 'name')

class BaggageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Baggage
        fields = ('total_weight', 'max_weight')