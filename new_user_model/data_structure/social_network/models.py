from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    friends = models.ManyToManyField('self')
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    email = models.CharField(max_length=100, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birth_date = models.DateField(max_length=10)
    gender = models.CharField(max_length=8)
    mobile_number = models.CharField(max_length=15)

    def __str__(self):
        return self.first_name + " " + self.last_name

