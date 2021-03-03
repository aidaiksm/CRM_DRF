from django.db import models
from flights.models import Flight
from users.models import MyUser


class Report(models.Model):
    OVERALL_RATED = [
        ('M', 'meet'),
        ('E', 'exceed'),
        ('IR', 'improvement required'),
    ]
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='report')
    created_at = models.DateTimeField(auto_now_add=True)
    flight_num = models.ForeignKey(Flight, on_delete=models.CASCADE)
    body = models.TextField()
    suggestions = models.TextField()
    evaluation = models.CharField(max_length=2, choices=OVERALL_RATED)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)

    def __str__(self):
        return f"{self.author}, {self.flight_num}"


class Comment(models.Model):
    report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name='comment')
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    feedback = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)



class Status(models.Model):
    STATUS = [
        ('PROCESSED', 'processed'),
        ('PENDING', 'pending'),
    ]
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    report = models.ForeignKey(Report, on_delete=models.CASCADE)
    status = models.CharField(max_length=255, choices=STATUS)