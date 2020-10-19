Feature: List UserProfile objects.

  Scenario: Get a list of all users.
    Given we have viewset for retrieving a list of users.
     When we input URL.
     Then we send a GET request in order to retrieve a list of users.