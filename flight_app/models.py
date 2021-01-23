from django.db import models

# Create your models here.
from data_base_course_work_backend.auth_app.models import Company, Employee
from data_base_course_work_backend.booking.models import Passenger


class Aircraft(models.Model):
    id = models.CharField(primary_key=True, max_length=10)
    location = models.CharField(max_length=4, blank=True, null=True)
    owner = models.ForeignKey(Company, models.DO_NOTHING, blank=True, null=True)
    model = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'aircraft'

class Flight(models.Model):
    aircraft = models.ForeignKey(Aircraft, models.DO_NOTHING)
    schedule_departure = models.DateTimeField()
    schedule_arrival = models.DateTimeField()
    actual_departure = models.DateTimeField(blank=True, null=True, )
    actual_arrival = models.DateTimeField(blank=True, null=True)
    status = models.TextField()  # This field type is a guess.
    departure_airport = models.CharField(max_length=4)
    arrival_airport = models.CharField(max_length=4)

    class Meta:
        managed = False
        db_table = 'flight'





class Seat(models.Model):
    number = models.CharField(max_length=3)
    flight = models.ForeignKey(Flight, models.DO_NOTHING)
    class_field = models.TextField(db_column='class')  # Field renamed because it was a Python reserved word. This field type is a guess.

    class Meta:
        managed = False
        db_table = 'seat'



class Booking(models.Model):
    total_amount = models.IntegerField(blank=True, null=True)
    time_limit = models.DateTimeField(blank=True, null=True)
    contact_data = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'booking'


class Ticket(models.Model):
    passenger = models.ForeignKey(Passenger, models.DO_NOTHING, blank=True, null=True)
    seat = models.ForeignKey(Seat, models.DO_NOTHING)
    amount = models.FloatField()
    book = models.ForeignKey(Booking, models.DO_NOTHING, blank=True, null=True)
    registered = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'ticket'



class TripPrice(models.Model):
    company_name = models.OneToOneField(Company, models.DO_NOTHING, db_column='company_name', primary_key=True)
    departure_airport = models.CharField(max_length=4)
    arrival_airport = models.CharField(max_length=4)
    price = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'trip_price'
        unique_together = (('company_name', 'departure_airport', 'arrival_airport', 'price'),)