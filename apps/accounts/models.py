from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import pre_save


class User(AbstractUser):
    mobile = models.CharField(max_length=11, blank=True, null=True, verbose_name="تلفن همراه")
    is_active = models.BooleanField(default=True, verbose_name="فعال / غیر فعال")

    def __str__(self):
        return self.username


def user_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.username:
        instance.username = instance.email

    if not instance.email:
        instance.email = instance.username


pre_save.connect(user_pre_save_receiver, sender=User)
