Feature: Register Feature

  Scenario: New User Registration
    Given I am on the registration page
    When I fill in the registration form with valid data
      | firstname | lastname | email                | password          |
      | John       | Doe       | john.doe@example.com | securepassword123! |
    And I submit the form
    Then I validate the registration
