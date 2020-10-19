Feature: Delete a Book object.

  Scenario: Delete a book.
    Given we have viewset for deleting a book.
     When we input book id parameter in the URL next to base /books/ URL.
     Then we click DELETE and delete a book.
