# Author: Ivana Ozakovic
# Created: 15/10/2020
# urls.py
"""books_app URL Configuration


"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from books_app.views import BooksViewSet, UserProfileViewSet

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register(r'users', UserProfileViewSet)     # Base URL: /books_app/users/
router.register(r'books', BooksViewSet)           # Base URL: /books_app/books/


urlpatterns = [
    path('admin/', admin.site.urls),
    path('books_app/', include(router.urls)),

]
