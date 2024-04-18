from django.db import models


# Create your models here.

class WxUsers(models.Model):
    openid = models.CharField(max_length=255, unique=True)
    nickname = models.CharField(max_length=255, blank=True)
    avatar_url = models.URLField(blank=True)

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
