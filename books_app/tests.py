# Author: Ivana Ozakovic
# Created: 15/10/2020
# tests.py
from http import HTTPStatus
from django.conf import settings
from django.test import TestCase, RequestFactory
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from books_app.models import UserProfile, Book
from books_app.views import UserProfileViewSet, BooksViewSet

class UserProfileTestCase(TestCase):
    """Test cases for UserProfile viewsets.
    """
    fixtures = ['initial_data.json',]
    def setUp(self):
        self.user = User.objects.create_user(
            pk=50,
            first_name='First',
            username='Username',
            password='Password',
            email='test_user@test.com'
        )
        self.userprofile, created = UserProfile.objects.get_or_create(
            pk=50,
            first_name='First',
            username='Username',
            password='Password',
            email='test_user@test.com',
            country='AU',
            user=self.user
        )
        from django.core.management import call_command
        data = call_command('loaddata', 'fixtures/initial_data.json', verbosity=0)
        assertEqual(1,0)
        print(data)

        

    ### Test for CREATE ###
    def test_userprofile_viewset_create(self):
        # self.setUp()
        self.test_profile = UserProfile.objects.create(
            first_name='Ivana',
            username='ivana-test',
            email='ivana@test.com',
            country='AU',
            password='testpassword',
            user=self.user
        )
        data = json.dumps({
            "title": "",
            "author": "",
            "isbn": "9780575099968"
        })
        # Setup APIClient
        client = APIClient()
        client.force_authenticate(user=self.user)
        response = client.post('/books_app/users/', data=data, content_type='application/json')

        print(response)
        # Check if you get a 200 back:
        self.assertEqual(response.status_code, HTTPStatus.OK._value_)
        # Check to see if isbn was created
        self.assertEqual(response.data['results']['isbn'], '9780575099968')
        pass

    ### Test for RETRIEVE ###
    def test_book_viewset_retrieve(self):
        request = self.factory.get('/books_app/books/1/')
        force_authenticate(request, user=self.user)
        response = BookViewSet.as_view({'get': 'list'})(request)
        # Check if the first dog's name is Balto, like it is in the fixtures:
        self.assertEqual(response.data['results'][0]['name'], 'Balto')
        # Check if you get a 200 back:
        self.assertEqual(response.status_code, HTTPStatus.OK._value_)
        pass

    ### Test for LIST ###
    def test_userprofile_viewset_list(self):
        pass

    ### Test for DELETE ###
    def test_userprofile_delete(self):
        pass


class BookTestCase(TestCase):
    """Test cases for Books viewsets.
    """
    def setUp(self):
        self.factory = RequestFactory()
        
        self.user = User.objects.create_superuser(
            first_name='Test',
            username='test_user',
            password='testpassword',
            email='test_user@test.com'
        )

        self.userprofile = UserProfile.objects.create(
            first_name='Test',
            username='test_user',
            password='testpassword',
            email='test_user@test.com',
            country='AU',
            user=self.user
        )

        client = APIClient()
        response = client.post('/books_app/books/', data=data, content_type='application/json')
        force_authenticate(request, user=self.user)

    ### Test for CREATE ###
    def test_book_viewset_create(self):
        self.book = Book.objects.create(
            title='Book',
            author='test_user',
            isbn='',
            user=self.user
        )
        data = json.dumps({
            "title": "",
            "author": "",
            "isbn": "9780575099968"
        })
        client = APIClient()
        client.force_authenticate(user=self.user)
        response = client.post('/books_app/books/', data=data, content_type='application/json')
        # Check if you get a 200 back:
        self.assertEqual(response.status_code, HTTPStatus.OK._value_)
        # Check to see if isbn was created
        self.assertEqual(response.data['results']['isbn'], '9780575099968')
        pass

    ### Test for RETRIEVE ###
    def test_book_viewset_retrieve(self):
        request = self.factory.get('/books_app/books/1/')
        force_authenticate(request, user=self.user)
        response = BookViewSet.as_view({'get': 'list'})(request)
        # Check if the first dog's name is Balto, like it is in the fixtures:
        self.assertEqual(response.data['results'][0]['name'], 'Balto')
        # Check if you get a 200 back:
        self.assertEqual(response.status_code, HTTPStatus.OK._value_)
        pass

    ### Test for LIST ###
    def test_book_viewset_list(self):
        pass

    ### Test for DELETE ###
    def test_book_viewset_delete(self):
        pass

    def test_validate_book_by_isbn(self):
        pass

    def test_validate_book_by_title(self):
        pass