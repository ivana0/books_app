# Author: Ivana Ozakovic
# Created: 15/10/2020
# serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from books_app.models import UserProfile, Book
from django_countries.serializers import CountryFieldMixin
from django_countries.serializer_fields import CountryField

class UserProfileSerializer(CountryFieldMixin, serializers.ModelSerializer):
    '''UserProfile serializer.'''
    class Meta:
        model = UserProfile
        fields = (
            'pk',
            'username',
            'first_name',
            'email',
            'password',
            'country'
        )

class BookSerializer(serializers.ModelSerializer):
    '''Book serializer.'''
    class Meta:
        model = Book
        fields = (
            'pk',
            'title',
            'author',
            'ISBN',
            'date_added'
        )

