# Additional Test Instructions

## Test Environment
- Base URL: https://example.com
- Test Environment: Staging
- Browser: Chromium

## API Interception & Response Handling

### Background: "I am on the login page"
```typescript
// Intercept and store user profile API response
await page.route('**/api/user/profile', async (route) => {
  const response = {
    status: 200,
    data: {
      name: "John Doe",
      email: "user@example.com",
      preferences: { theme: "light" }
    }
  };
  await route.fulfill({ json: response });
  world.saveResponse('userProfile', response);
});
```

### Scenario: "Successful login with valid credentials"
1. When entering credentials:
   ```json
   // testdata/users.json
   {
     "validUser": {
       "email": "user@example.com",
       "password": "validPassword123"
     }
   }
   ```

2. For login button click:
   ```typescript
   // Intercept login API call
   await page.route('**/api/auth/login', async (route) => {
     const response = {
       status: 200,
       data: {
         token: "jwt.token.here",
         user: {
           id: "123",
           name: "John Doe",
           email: "user@example.com"
         }
       }
     };
     await route.fulfill({ json: response });
     world.saveResponse('loginSuccess', response);
   });
   ```

3. For dashboard redirect validation:
   ```typescript
   // Read saved login response
   const loginResponse = world.getResponse('loginSuccess');
   // Verify user ID in URL matches response
   expect(page.url()).toContain(`/dashboard/${loginResponse.data.user.id}`);
   ```

4. For welcome message:
   ```typescript
   const userProfile = world.getResponse('userProfile');
   await expect(page.locator('[data-testid="welcome-message"]'))
     .toContainText(userProfile.data.name);
   ```

### Scenario: "Failed login with invalid credentials"
1. For invalid login attempt:
   ```typescript
   await page.route('**/api/auth/login', async (route) => {
     const response = {
       status: 401,
       error: {
         code: "AUTH_FAILED",
         message: "Invalid email or password"
       }
     };
     await route.fulfill({ 
       status: 401,
       json: response 
     });
     world.saveResponse('loginError', response);
   });
   ```

2. For error message validation:
   ```typescript
   const errorResponse = world.getResponse('loginError');
   await expect(page.locator('[data-testid="error-message"]'))
     .toContainText(errorResponse.error.message);
   ```

## Test Data Structure
```json
// testdata/test_data.json
{
  "users": {
    "valid": {
      "email": "user@example.com",
      "password": "validPassword123",
      "name": "John Doe"
    },
    "invalid": {
      "email": "user@example.com",
      "password": "wrongPassword"
    }
  },
  "api": {
    "endpoints": {
      "login": "/api/auth/login",
      "profile": "/api/user/profile"
    }
  }
}
```

## Special Requirements
1. API Response Handling:
   - Use `world.saveResponse(key, response)` for storing responses
   - Use `world.getResponse(key)` for retrieving stored responses
   - Clear responses between scenarios using `world.clearResponses()`

2. Test Data Management:
   - Load test data from JSON files in `testdata/` directory
   - Use type-safe interfaces for test data objects
   - Support environment-specific test data overrides

3. API Interception:
   - Mock all external API calls
   - Save both request and response data
   - Support dynamic response generation based on request data

## Page Object Guidelines
- Use data-testid attributes for element selection
- Include retry logic for dynamic elements
- Add custom error messages for failed assertions
- Implement response interception in page object methods

## Test Coverage Requirements
- Handle network errors gracefully
- Add password visibility toggle testing
- Include form validation checks
- Test "Remember Me" functionality

## Notes
- The login endpoint is rate-limited to 5 requests per minute
- Password field should be masked in test logs
- Screenshots should be taken on test failures
- Clear stored responses in World object between scenarios 