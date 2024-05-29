from django.db import models

# Create your models here.
# models.py
from django.db import models

class Student(models.Model):
    id = models.IntegerField(primary_key=True)
    student_id = models.CharField(max_length=20)
    name = models.CharField(max_length=50)
    class_year = models.CharField(max_length=10)
    class_name = models.CharField(max_length=50)
    gender = models.CharField(max_length=10)
    contact = models.CharField(max_length=15)
    dorm_building = models.CharField(max_length=10)
    dorm_number = models.CharField(max_length=10)
    status = models.CharField(max_length=10)
    advisor = models.CharField(max_length=50)
    counselor = models.CharField(max_length=50)
    notes = models.CharField(max_length=50)

    def __str__(self):
        return self.name