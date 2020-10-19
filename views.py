# Author: Ivana Ozakovic
# Created: 15/10/2020
# views.py
import requests
import json
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import permissions
from books_app.serializers import BookSerializer, UserProfileSerializer
from books_app.models import Book, UserProfile
from django.contrib.auth.models import User
from django.http import Http404
from rest_framework import status
from datetime import datetime, timedelta

###########   USERPROFILE VIEWSET    ###########
class UserProfileViewSet(viewsets.ModelViewSet):
    '''UserProfileViewSet API automatically provides 
    `LIST`, `CREATE`, `RETRIEVE`, and `DESTROY` actions.
    
    URLs:
    /books_app/users/
    /books_app/users/<pk>/
    '''
    http_method_names = ['get', 'post', 'head', 'delete']
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        '''Action that LISTS all UserProfile objects.
        '''
        queryset = self.queryset if self.queryset else None
        # Check if superuser created without UserProfile instance.
        # ^ in case we need it when run it the first time usually.
        superuser = User.objects.filter(is_superuser=True)
        # For every superuser without UserProfile instance, create one.
        for user in superuser:
            if user.userprofile is None:
                    user_profile, created = UserProfile.objects.get_or_create(
                    first_name=first_name,
                    username=user.username,
                    email=email,
                    country=country,
                    password=user.password,
                    user=user
                )

        if queryset is None:
            Response(
                    {"detail": "No users."}, 
                    status=status.HTTP_204_NO_CONTENT
                )

        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        '''Action that CREATES a new UserProfile objects,
        but also creates a new relevant user for django auth.
        '''
        request_data = request.data

        # Create User object for each UserProfile
        user = User.objects.create_user(
            first_name=request_data['first_name'],
            username=request_data['username'],
            email=request_data['email'],
            password=request_data['password'],
        )

        # If not created, reutrn bad request and message
        if user is None:
            return Response({"detail": "Failed to create user."}, status=status.HTTP_400_BAD_REQUEST)

        # Create UserProfile object linking it to previously created user object
        user_profile, created = UserProfile.objects.get_or_create(
            first_name=request_data['first_name'],
            username=request_data['username'],
            email=request_data['email'],
            country=request_data['country'],
            password=request_data['password'],
            user=user
        )
        # If not created, reutrn bad request and message
        if not created:
            return Response({"detail": "Failed to create user."}, status=status.HTTP_400_BAD_REQUEST)

        # Serialize data
        data = UserProfileSerializer(user_profile).data
        return Response(
            data={'error': False, 'message': "User object successfully created.", 'results': data},
            status=status.HTTP_201_CREATED
            )

    def destroy(self, request, *args, **kwargs):
        '''Action that DESTROYS a UserProfile instance,
        but also deletes a relevant User instance.
        '''
        instance = self.get_object()
        try:
            self.perform_destroy(instance)
        except Http404:
            return Response(
                data={'message': "Could not destroy the instance / Nothing to destroy."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Get User object and delete it
        try:
            user_instance = User.objects.filter(id=instance.user.id)
        except:
            # Return no content if no instance returned
            return Response(status=status.HTTP_204_NO_CONTENT)

        user_instance.delete()                              # Delete user instance
        return Response(status=status.HTTP_200_OK)          # Return status 200

    def retrieve(self, request, pk=None):
        '''Method that RETRIEVES a UserProfile instance.
        '''
        # Try retrieving UserProfile instance
        try:
            user = UserProfile.objects.get(pk=pk)
        except UserProfile.DoesNotExist:
            user = None
            return Response(
                data={'error': True, 'message': "User does not exist.", 'results': "None"},
                status=status.HTTP_204_NO_CONTENT
                )

        # Serialize data
        data = UserProfileSerializer(user).data
        # Return response status code 200
        return Response(
            data={'error': False, 'message': "User object successfully retrieved.", 'results': data},
            status=status.HTTP_200_OK
            )

###########   BOOKS VIEWSET    ###########
class BooksViewSet(viewsets.ModelViewSet):
    '''BooksViewSet API viewset automatically provides
    `LIST`, `CREATE`, `RETRIEVE`, and `DESTROY` actions.
    
    URLs:
        /books_app/books/
        /books_app/books/<pk>/     
        /books_app/books/?days_ago=<int>
    '''
    http_method_names = ['get', 'post', 'head', 'delete']
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def validate_book_by_isbn(self, isbn):
        '''Validate if books exist using ISBN provided via Google Books API.

        Parameters:
            isbn(str): Industry identifier - 10 digit number.
        Returns:
                json:   Book data from the response.
        '''
        # Create getting started variables
        base_api = "https://www.googleapis.com/books/v1/volumes?q=isbn:"
        # Send a request and get a JSON response
        response = requests.get(base_api + str(isbn))
        
        return self.parse_response(response)

    def validate_book_by_title(self, title):
        '''Validate if books exist using ISBN provided via Google Books API.

        Parameters:
            isbn(str): Industry identifier - 10 digit number.
        Returns:
                json:   Book data from the response.
        '''
        # Create getting started variables
        base_api = "https://www.googleapis.com/books/v1/volumes?q=title:"
        # Send a request and get a JSON response
        response = requests.get(base_api + str(title))

        return self.parse_response(response)

    def parse_response(self, response):
        # Parse JSON into Python as a dictionary
        response_dict = json.loads(response.text)
        
        # Get details from the structure in response
        book_items = response_dict['items']
        book_items = book_items[0]

        # Get volume info details to get title, isbn, and authors
        volume_info = book_items['volumeInfo']
        return volume_info if volume_info else None


    def list(self, request, *args, **kwargs):
        '''Action that LISTS all Book objects for current user.
        '''
        # Retrieve current user from request
        user_id = self.request.user.id
        u = User.objects.filter(id=user_id).first()
        current_user = UserProfile.objects.filter(user=u).first()
        # Filter queryset to return books by current user
        query_set = self.queryset.filter(added_by=current_user)

        # If queryset empty
        if query_set is None:
            return Response(
                    {"detail": "No content."}, 
                    status=status.HTTP_204_NO_CONTENT
                )

        # Check if 'days_ago' parameter in url - e.g. /books_app/books/?days_ago=7
        days = self.request.GET.get('days_ago', None)

        # If "days_ago" in get parameter
        if days:
            # Get current datetime and get difference in last n days
            since = datetime.now()-timedelta(days=int(days))  
            # Filter queryset  
            query_set = query_set.filter(date_added__gte=since)

        # Else serialise and return data in response
        serializer = self.serializer_class(query_set, many=True)
        return Response(serializer.data)


    def create(self, request, *args, **kwargs):
        '''Action that CREATES a new Book object,
        but also creates a new relevant user for django auth.
        '''
        request_data = request.data

        isbn = request_data['ISBN'] if request_data['ISBN'] else None
        title = request_data['title'] if request_data['title'] else None
        if not isbn and not title:
            return Response(
                data={'error': True, 'message': "Please enter book ISBN and/or title.", 'results': 'None'},
                status=status.HTTP_404_NOT_FOUND)

        # Validate book data by isbn
        if isbn:
            isbn = str(isbn).strip(' -')
            book_data = self.validate_book_by_isbn(isbn)

        # Validate book data by title
        if title:
            title = str(title).strip(' ')
            title = title.lower()
            book_data = self.validate_book_by_title(title)
            # Get ISBN
            isbn = book_data['industryIdentifiers'][0]
            isbn = isbn['identifier']

        if not book_data:
            return Response(data={'error': True, 'message': "Invalid ISBN.", 'results': 'None'})

        # Set title and author
        title = book_data['title']
        author = book_data['authors']

        # Retrieve current user from request
        user_id = self.request.user.id
        u = User.objects.filter(id=user_id).first()
        current_user = UserProfile.objects.filter(user=u).first()
        # Create Book object
        book, created = Book.objects.get_or_create(
            title=title, 
            author=list(author),
            ISBN=isbn, 
            added_by=current_user
        )

        # Serialize data
        data = BookSerializer(book).data
        return Response(
            data={'error': False, 'message': "Book object successfully created.", 'results': data},
            status=status.HTTP_201_CREATED
            )

    def destroy(self, request, *args, **kwargs):
        '''Action that DESTROYS a UserProfile instance,
        but also deletes a relevant User instance.
        '''
        instance = self.get_object()
        try:
            self.perform_destroy(instance)
        except Http404:
            return Response(
                data={'error': True, 'message': "Could not destroy the instance / Nothing to destroy."},
                status=status.HTTP_404_NOT_FOUND)

        return Response(
            data={'error': False, 'message': "Book deleted."},
            status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        '''Method that RETRIEVES a Book instance.
        '''
        # Try retrieving Book instance
        try:
            book = Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            book = None
            return Response(
                data={'error': True, 'message': "Book does not exist."},
                status=status.HTTP_204_NO_CONTENT)

        # Serialize data
        data = BookSerializer(book).data
        # Return response status code 200
        return Response(
            data={'error': False, 'message': "Book object successfully retrieved.", 'results': data},
            status=status.HTTP_200_OK)


