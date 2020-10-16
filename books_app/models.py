# Author: Ivana Ozakovic
# Created: 15/10/2020
# models.py

from django.db import models
from django_countries.fields import CountryField
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
	first_name = models.CharField(max_length=50, null=False, blank=False)
	email = models.CharField(max_length=50, null=False, blank=False)
	country = CountryField()
	user = models.OneToOneField(User, on_delete=models.CASCADE)

# https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html#onetoone
# Hooking create_user_profile and save_user_profile
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Book(models.Model):
	title = models.CharField(max_length=100, null=False, blank=False)
	author = models.CharField(max_length=200, null=False, blank=False)
	ISBN = models.CharField(max_length=50, null=False, blank=False)
	date_added = models.DateTimeField(auto_now_add=True)
	added_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
