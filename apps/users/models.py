# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from ..comics.models import Series
from django.contrib.auth.models import UserManager, AbstractUser

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    store_location = models.CharField(
        max_length=50,
        choices = (
            ('LAGRANGE', 'La Grange'),
            ('OAKLAWN', 'Oak Lawn'),
        ),
        blank=True
    )
    subscriptions = models.ManyToManyField(Series)

@receiver(post_save, sender=User)
def update_subscriber_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
