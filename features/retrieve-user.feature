Feature: Retrieve a UserProfile object.

  Scenario: Retrieve a user.
    Given we have viewset for retrieving a user.
     When we input user id parameter in the URL next to base /users/ URL.
     Then we send a GET request in order to retrieve a relevant user.
