from django.db import models
from django.utils import timezone


class Products(models.Model):
    name = models.CharField(unique=True, max_length=100, null=False, blank=False)
    price = models.FloatField()
    image = models.ImageField(upload_to='images/', max_length=100)
    creator = models.CharField(max_length=100)
    create_date = models.DateTimeField(default=timezone.now())


class JSON(models.Model):
    content = models.JSONField()
