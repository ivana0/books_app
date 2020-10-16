# Author: Ivana Ozakovic
# Created: 15/10/2020
# views.py

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import permissions
from books_app.serializers import BookSerializer, UserProfileSerializer
from books_app.models import Book, UserProfile
from django.contrib.auth.models import User


class UserProfileViewSet(viewsets.ModelViewSet):
    '''UserProfileViewSet API automatically provides `list`, `create`, `retrieve`,
        `update` and `destroy` actions.

    This viewset allows user to create, view and delete users.
    '''
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return super(UserProfileViewSet, self).get_queryset()

    def list(self, request, *args, **kwargs):
        query_set = self.queryset
        # If queryset empty
        if query_set is None:
            return Response(
                    {"detail": "No content."}, 
                    status=status.HTTP_204_NO_CONTENT
                )

        # Else serialise and return data in response
        serializer = UserProfileSerializer(query_set, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        query_set = self.get_queryset()
        request_data = request.data

        user, created = UserProfile.objects.get_or_create(
            first_name=request_data['first_name'], 
            email=request_data['author'],
            country=request_data['country'],
        )
        # If not created, reutrn bad request and message
        if not created:
            return Response({"detail": "Failed to create user."}, status=status.HTTP_400_BAD_REQUEST)

        data = UserProfileSerializer(user).data
        return Response(
            data={'error': False, 'message': "User object successfully created", 'results': data},
            status=status.HTTP_201_CREATED
            )

    def destroy(self, request, *args, **kwargs):
        return Response({"detail": "Deleted."}, status=status.HTTP_200_OK)

class BooksViewSet(viewsets.ModelViewSet):
    '''BooksViewSet API viewset automatically provides `list`, `create`, `retrieve`,
        `update` and `destroy` actions.

    This viewset allows user to create, view and delete books.
    '''
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return super(BooksViewSet, self).get_queryset()

    def list(self, request, *args, **kwargs):
        query_set = self.queryset

        # If queryset empty
        if query_set is None:
            return Response(
                    {"detail": "No content."}, 
                    status=status.HTTP_204_NO_CONTENT
                )

        # Else serialise and return data in response
        serializer = BookSerializer(query_set, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        request_data = request.data
        book, created = Book.objects.get_or_create(
            title=request_data['title'], 
            author=request_data['author'],
            ISBN=request_data['ISBN'], 
            date_added=request_data['date_added'],
            added_by=request_data['added_by'],
        )

        if book is None:
            return Response(
                    {"detail": "Failed to create book."}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

        data = BookSerializer(book).data
        return Response(data={'error': False, 'message': "Book object successfully created", 'results': data})

    def destroy(self, request, *args, **kwargs):
        return Response({"detail": "Deleted."}, status=status.HTTP_200_OK)

