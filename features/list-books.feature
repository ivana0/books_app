Feature: Create a Book object.

  Scenario: Run a simple test
    Given we have viewset for creating a book.
     When we input parameters to POST in order to create a Book object.
     Then we click POST/CREATE and create a Book object.
