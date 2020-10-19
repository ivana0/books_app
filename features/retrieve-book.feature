Feature: Retrieve a Book object.

  Scenario: Retrieve a book.
    Given we have viewset for retrieving a book.
     When we input book id parameter in the URL next to base /books/ URL.
     Then we send a GET request in order to retrieve a relevant book.
