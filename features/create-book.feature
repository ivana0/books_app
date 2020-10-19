Feature: Create a Book object.

  Scenario: Create a valid book.
    Given we have viewset for creating a book.
     When we input parameters to POST/CREATE in order to create a book
     Then we click POST/CREATE and create a book.
