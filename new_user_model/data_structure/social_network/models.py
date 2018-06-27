from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    friends = models.ManyToManyField('self')
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    email = models.CharField(max_length=100, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birth_date = models.CharField(max_length=10)
    gender = models.CharField(max_length=8)
    mobile_number = models.CharField(max_length=15)

    def __str__(self):
        return self.first_name + " " + self.last_name


class Group(models.Model):
    name = models.CharField(max_length=100, unique=True)
    users = models.ManyToManyField(CustomUser, related_name="my_groups")

    def __str__(self):
        return self.name


class Mypost(models.Model):
    postbody = models.CharField(max_length=1000)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(CustomUser, related_name="my_likes")
    group = models.ForeignKey(Group, on_delete=models.CASCADE, default=None, blank=True, null=True)
