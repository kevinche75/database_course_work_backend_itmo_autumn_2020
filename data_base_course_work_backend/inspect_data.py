# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Aircraft(models.Model):
    id = models.CharField(primary_key=True, max_length=10)
    location = models.CharField(max_length=4, blank=True, null=True)
    owner = models.ForeignKey('Company', models.DO_NOTHING, blank=True, null=True)
    model = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'aircraft'





class Booking(models.Model):
    total_amount = models.IntegerField(blank=True, null=True)
    time_limit = models.DateTimeField(blank=True, null=True)
    contact_data = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'booking'


class Company(models.Model):
    name = models.CharField(primary_key=True, max_length=30)
    type = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'company'


class Crew(models.Model):
    employee = models.OneToOneField('Employee', models.DO_NOTHING, primary_key=True)
    flight = models.ForeignKey('Flight', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'crew'
        unique_together = (('employee', 'flight'),)




class Flight(models.Model):
    aircraft = models.ForeignKey(Aircraft, models.DO_NOTHING)
    schedule_departure = models.DateTimeField()
    schedule_arrival = models.DateTimeField()
    actual_departure = models.DateTimeField(blank=True, null=True)
    actual_arrival = models.DateTimeField(blank=True, null=True)
    status = models.TextField()  # This field type is a guess.
    departure_airport = models.CharField(max_length=4)
    arrival_airport = models.CharField(max_length=4)

    class Meta:
        managed = False
        db_table = 'flight'


class GateSchedule(models.Model):
    employee = models.ForeignKey(Employee, models.DO_NOTHING, blank=True, null=True)
    flight = models.ForeignKey(Flight, models.DO_NOTHING, blank=True, null=True)
    gate_number = models.SmallIntegerField()
    start_time = models.DateTimeField()
    finish_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'gate_schedule'


class Passenger(models.Model):
    passport_no = models.CharField(primary_key=True, max_length=10)
    name = models.CharField(max_length=30)
    second_name = models.CharField(max_length=30)
    third_name = models.CharField(max_length=30, blank=True, null=True)
    birthday = models.DateField()

    class Meta:
        managed = False
        db_table = 'passenger'








class ReceptionSchedule(models.Model):
    employee = models.ForeignKey(Employee, models.DO_NOTHING, blank=True, null=True)
    flight = models.ForeignKey(Flight, models.DO_NOTHING, blank=True, null=True)
    reception_number = models.SmallIntegerField()
    start_time = models.DateTimeField()
    finish_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'reception_schedule'






class Seat(models.Model):
    number = models.CharField(max_length=3)
    flight = models.ForeignKey(Flight, models.DO_NOTHING)
    class_field = models.TextField(db_column='class')  # Field renamed because it was a Python reserved word. This field type is a guess.

    class Meta:
        managed = False
        db_table = 'seat'






