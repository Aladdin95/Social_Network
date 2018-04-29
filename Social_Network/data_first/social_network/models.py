from django.db import models


class User(models.Model):
    friends = models.ManyToManyField('self')
    First_name = models.CharField(max_length=100)
    Last_name = models.CharField(max_length=100)
    Birth_date = models.CharField(max_length=100)
    gender = models.CharField(max_length=100)
    Mobile_number = models.CharField(max_length=100)

    def __str__(self):
        return self.First_name + " " + self.Last_name

