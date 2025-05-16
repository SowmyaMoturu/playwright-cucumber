Feature: User Login
  As a registered user
  I want to log in to my account
  So that I can access my personalized content

  Background:
    Given I am on the login page

  Scenario: Successful login with valid credentials
    When I enter my email "user@example.com"
    And I enter my password "validPassword123"
    And I click the login button
    Then I should be redirected to the dashboard
    And I should see a welcome message with my name

  Scenario: Failed login with invalid credentials
    When I enter my email "user@example.com"
    And I enter my password "wrongPassword"
    And I click the login button
    Then I should see an error message "Invalid email or password"
    And I should remain on the login page 