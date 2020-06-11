from django.db import models
from django.contrib.auth.models import User
from django_project import settings

# Create your models here.
class InvoiceDB(models.Model):
    number = models.CharField(max_length=64)
    date = models.DateField()
    name = models.CharField(max_length=64)
    total_tcc = models.FloatField(null=True, blank=True, default=None)
    total_vat = models.FloatField(null=True, blank=True, default=None)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    class Meta:
        unique_together = ["number", "user"]
