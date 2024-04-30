from django.db import models

import time


# Create your models here.

class WxUsers(models.Model):
    openid = models.CharField(max_length=255, unique=True)
    nickname = models.CharField(max_length=255, blank=False, null=False, default=f'User_{time.time()}')
    avatar_url = models.URLField(blank=True)
    cart = models.JSONField(default={})
    order = models.JSONField(default={
        'ongoing': {},
        'servicing': {},
        'completed': {},
    })

    def __str__(self):
        return self.openid


# class TokenLibrary(models.Model):
#     openid = models.CharField(max_length=255, unique=True)
#     refresh_token = models.TextField()
#     access_token = models.TextField()
#     expiration = models.BigIntegerField()
#     safe_level = models.IntegerField(default=5)
#
#     def __str__(self):
#         return self.openid
