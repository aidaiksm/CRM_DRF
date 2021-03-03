from django.db import models
from users.models import MyUser


class Flight(models.Model):
    code = models.CharField(max_length=255)
    destination = models.CharField(max_length=255)
    date = models.DateTimeField()
    layover = models.BooleanField(default=False)
    crew = models.ManyToManyField(MyUser)

    def __str__(self):
        return f'{self.destination} / {self.date}'