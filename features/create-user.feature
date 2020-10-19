Feature: Create a UserProfile object.

  Scenario: Create a valid user profile.
    Given we have viewset for creating a user.
     When we input parameters to POST/CREATE in order to create a user profile.
     Then we click POST/CREATE and create a user profile.
