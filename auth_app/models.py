from django.db import models

# Create your models here.

class Company(models.Model):
    name = models.CharField(primary_key=True, max_length=30)
    type = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'company'


class Employee(models.Model):
    passport_no = models.CharField(primary_key=True, max_length=10, db_column='passport_no')
    company = models.ForeignKey(Company, on_delete=models.DO_NOTHING, db_column='company')
    name = models.CharField(max_length=30)
    second_name = models.CharField(max_length=30)
    third_name = models.CharField(max_length=30, blank=True, null=True)
    position = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'employee'
