from datetime import timedelta, date, datetime

from django.db import models


# Create your models here.

class Cycle(models.Model):
    previous_date = models.DateField()
    cycle_length = models.PositiveIntegerField()
    next_occurrence = models.DateField()
    next_12_occurrences = models.TextField()
    ovulation_date = models.DateField()
    flow_date = models.DateField()
    safe_periods = models.TextField()
