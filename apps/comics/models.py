# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class SeriesManager(models.Manager):
    def subscribe(self, id, user):
        errors = []
        try:
            series = self.get(id=id)
            user.profile.subscriptions.add(series)
            user.profile.save()
            return (True, series)
        except:
            errors.append("Did not subscribe successfully")
            return (False, errors)
    def unsubscribe(self, id, user):
        errors = []
        try:
            series = self.get(id=id)
            user.profile.subscriptions.remove(series)
            user.profile.save()
            return (True, series)
        except:
            errors.append("Did not unsubscribe successfully")
            return (False, errors)

class Series(models.Model):
    title = models.CharField(max_length=255)
    publisher = models.CharField(max_length=35)
    description = models.CharField(max_length=1000, blank=True)
    active = models.BooleanField(default=True)
    series_code = models.CharField(max_length=25)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = SeriesManager()

    @property
    def latest_issue(self):
        return self.issue_set.latest('ship_date')

    def __unicode__(self):
        return self.title

class Issue(models.Model):
    title = models.CharField(max_length=255)
    series_code = models.CharField(max_length=25)
    number = models.IntegerField()
    publisher = models.CharField(max_length=50)
    ship_date = models.DateField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    writer = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    colorist = models.CharField(max_length=255, blank=True)
    cover_image = models.ImageField('jpg', upload_to='comics/issues', blank=True)
    description = models.TextField()
    series = models.ForeignKey(Series)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.title

class Review(models.Model):
    content = models.TextField()
    series = models.ForeignKey(Series, blank=True, null=True)
    issue = models.ForeignKey(Issue, blank=True, null=True)
    user = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Comment(models.Model):
    content = models.TextField()
    review = models.ForeignKey(Review)
    user = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
