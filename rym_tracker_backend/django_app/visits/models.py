from django.db import models


class VisitsLog(models.Model):
    is_unique = models.BooleanField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"is_unique: {self.is_unique}, timestamp: {self.timestamp}"
