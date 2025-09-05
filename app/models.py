from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    PRIORITY_CHOICES = [
        ('high', 'Високий'),
        ('medium', 'Середній'),
        ('low', 'Низький')
    ]   

    text = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, default="В процесі")
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES)
    deadline = models.DateField()
    add_date = models.DateField(auto_now_add=True)
    add_time = models.TimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.owner}, {self.add_date}"


class Comment(models.Model):
    text = models.TextField()
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    add_datetime = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['add_datetime']
