from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Glucose(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    glucose_level = models.DecimalField(max_digits=7, decimal_places=2)
    entry_date = models.DateField()

    class Meta:
        verbose_name = 'Glucose Level'
        verbose_name_plural = 'Glucose Level'

    def __str__(self):
        return f'{self.user.username} - {self.glucose_level} kg on {self.entry_date}'