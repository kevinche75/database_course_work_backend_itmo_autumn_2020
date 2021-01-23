from django.db import models

# Create your models here.
class Passenger(models.Model):
    passport_no = models.CharField(primary_key=True, max_length=10)
    name = models.CharField(max_length=30)
    second_name = models.CharField(max_length=30)
    third_name = models.CharField(max_length=30, blank=True, null=True)
    birthday = models.DateField()

    class Meta:
        managed = False
        db_table = 'passenger'