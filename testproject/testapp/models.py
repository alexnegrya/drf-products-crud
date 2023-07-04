from django.db import models
from django.utils import timezone


class Products(models.Model):
    name = models.CharField(unique=True, max_length=100, null=False, blank=False)
    price = models.FloatField()
    image_url = models.CharField(max_length=100000)
    creator = models.CharField(max_length=100)
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.pk})"
