from django.db import models

# Create your models here.


class AdminUser(models.Model):
    name = models.CharField(max_length=255)
    account = models.BigIntegerField()
    password = models.CharField(max_length=255)
    avatar = models.TextField()

    def __str__(self):
        return self.name
