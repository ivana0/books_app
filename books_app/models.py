# Author: Ivana Ozakovic
# Created: 15/10/2020
# models.py
from django.db import models
from django_countries.fields import CountryField
from django_countries import countries
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    '''UserProfile model that extends standard django user model.
    '''
    first_name = models.CharField(max_length=100, null=False, blank=False)
    username = models.CharField(max_length=100, null=False, blank=False)
    email = models.CharField(max_length=100, null=False, blank=False)
    password = models.CharField(max_length=100)
    country = CountryField(null=False, blank=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.first_name

class Book(models.Model):
    '''Book model.
    '''
    title = models.CharField(max_length=100, null=False, blank=False)
    author = models.CharField(max_length=200, null=False, blank=False)
    ISBN = models.CharField(max_length=50, null=False, blank=False)
    date_added = models.DateTimeField(auto_now_add=True)
    added_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
