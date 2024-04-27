from django.db import models


# Create your models here.

class MainPageImages(models.Model):
    name = models.CharField(max_length=200)
    url = models.TextField()


class Commodity(models.Model):
    unique_id = models.IntegerField()
    com_name = models.TextField()
    com_introduce = models.TextField()
    com_price = models.FloatField()
    com_reserve = models.IntegerField()
    com_banners = models.JSONField()
    com_introduction_pictures = models.JSONField()
    com_is_active = models.BooleanField(default=True)
    com_is_preferential = models.BooleanField(default=True)
    com_is_coupon = models.BooleanField(default=True)


class OrderForm(models.Model):
    openid = models.CharField(max_length=255, unique=True)
    ongoing_order = models.JSONField()
    service_order = models.JSONField()
    closed_order = models.JSONField()

