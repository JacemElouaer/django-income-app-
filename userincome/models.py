from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Income(models.Model):
    amount = models.FloatField()
    date = models.DateField()
    description = models.TextField()
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    source = models.CharField(max_length=255)

    def __str__(self):
        return str(self.id)

    class Meta:
        ordering = ['-date']


class Source(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
