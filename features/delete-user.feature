Feature: Delete a UserProfile object.

  Scenario: Delete a user.
    Given we have viewset for deleting the user.
     When we input user id parameter in the URL next to base /users/ URL.
     Then we click DELETE and delete the user.
