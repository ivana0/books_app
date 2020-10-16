# Author: Ivana Ozakovic
# Created: 15/10/2020
# serializers.py

from rest_framework import serializers
from django.contrib.auth.models import User

from books_app.models import UserProfile, Book

class UserProfileSerializer(serializers.ModelSerializer):
    '''UserProfile serializer.'''
    # id = serializers.IntegerField(source='pk', read_only=True)
    # email = serializers.SerializerMethodField()
    # id = serializers.IntegerField(source='pk', read_only=True)
    first_name = serializers.CharField(source='user.first_name')
    email = serializers.CharField(source='user.email')
    # password = serializers.CharField(max_length=128, source='user.password,read_only=True')
    # first_name = serializers.SerializerMethodField()
    # email = serializers.SerializerMethodField()
    # country = serializers.SerializerMethodField()
    # user = serializers.SerializerMethodField()
    # country = serializers.UserProfileSerializer('country')
    class Meta:
        model = UserProfile
        fields = (
            'first_name',
            'email',
            'country'
        )

    def get_first_name(self, obj):
        return obj.first_name

    def get_email(self, obj):
        return obj.email

    def get_country(self, obj):
        return obj.country

class BookSerializer(serializers.ModelSerializer):
    '''Book serializer.'''
    class Meta:
        model = Book
        fields = (
            'title',
            'author',
            'ISBN',
            'date_added',
            'added_by'
        )