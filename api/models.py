from django.db import models


# Create your models here.

class MainPageImages(models.Model):
    name = models.CharField(max_length=200)
    url = models.TextField()
