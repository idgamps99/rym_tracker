import datetime
from django.db import models
from django.utils import timezone


class VisitsLog(models.Model):
    is_unique = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Unique visit: {self.is_unique}, Timestamp: {self.timestamp}"
