from django.db import models
from django.utils import timezone


class VisitsLog(models.Model):
    is_unique = models.BooleanField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"IsUnique: {self.is_unique}, Datetime: {self.timestamp}"
