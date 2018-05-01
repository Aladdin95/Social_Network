from django.db import models


class User(models.Model):
    friends = models.ManyToManyField('self')
    username = models.CharField(max_length=100)
    password = models.CharField(max_length =100)
    email = models.CharField(max_length=100,unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birth_date = models.CharField(max_length=100)
    gender = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=100)


    def __str__(self):
        return self.first_name + " " + self.last_name

