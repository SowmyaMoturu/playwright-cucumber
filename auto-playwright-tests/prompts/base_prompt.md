# Test Generation Instructions

## Framework Configuration
```yaml
framework: playwright
language: typescript
project_structure: |
  src/
    features/        # Cucumber feature files
    pages/          # Page object models
      basepage.ts   # Base page with common utilities
    step-definitions/  # Step definition files
    api.calls/      # API interaction helpers
    setup/          # Test setup and configuration
      world.ts      # Test context and shared utilities
    utils/          # Helper functions and utilities
```

## Core Patterns

1. **Response Handling Patterns**:
   ```typescript
   // Pattern 1: Direct Response Handling
   async waitForResponse(url: string, method: string, timeout = 60000) {
       try {
           const response = await page.waitForResponse(response =>
               response.url().includes(url) 
                   && response.request().method() === method
                   && (response.request().resourceType() === 'xhr' || response.request().resourceType() === 'fetch'),
               { timeout: timeout }
           );
           return await response.json();
       } catch (error) {
           throw new Error(`Failed to receive response for URL: ${url} with method: ${method} within ${timeout}ms timeout`);
       }
   }

   // Pattern 2: Response Promise for Pre-setup
   getResponsePromise(url: string, method: string, timeout = 60000) {
       return page.waitForResponse(response =>
           response.url().includes(url) 
               && response.request().method() === method
               && (response.request().resourceType() === 'xhr' || response.request().resourceType() === 'fetch'),
           { timeout: timeout }
       );
   }
   ```

2. **State Management with ScenarioWorld**:
   ```typescript
   // Store API responses
   this.apiResponse = await pageObjects.BasePage.waitForResponse('/api/data', 'GET');
   
   // Store form data
   this.formData = dataTable.hashes()[0];
   
   // Store multiple responses
   this.responses = {
       user: await userPromise.json(),
       settings: await settingsPromise.json()
   };
   ```

3. **Page Object Pattern**:
   ```typescript
   export class PageName extends BasePage {
       private readonly locators = {
           elements: '[data-test="element-name"]',
           form: {
               inputs: '[data-test="form-input"]',
               submit: '[data-test="submit-btn"]'
           }
       };

       async performAction() {
           await this.waitForElement(this.locators.elements);
           await this.click(this.locators.form.submit);
       }
   }
   ```

4. **Error Handling**:
   ```typescript
   try {
       await this.waitForElement(selector);
       await this.click(selector);
   } catch (error) {
       if (error.message.includes('timeout')) {
           throw new Error(`Element not clickable: ${selector}`);
       }
       throw error;
   }
   ```

## Best Practices

1. **Response Handling**:
   - Use Pattern 1 (waitForResponse) for simple, single API calls
   - Use Pattern 2 (getResponsePromise) for multiple concurrent calls or timing-critical operations
   - Always set up response listeners BEFORE triggering actions
   - Store responses in ScenarioWorld for later use
   - Use typed interfaces for response data

2. **Page Objects**:
   - Use data-test attributes for selectors
   - Group locators by functionality
   - Implement reusable action methods
   - Extend BasePage for common utilities
   - Use strong TypeScript typing

3. **State Management**:
   - Store all test data in ScenarioWorld
   - Use typed interfaces for stored data
   - Clear state between scenarios
   - Document stored data structure

4. **Error Handling**:
   - Use explicit timeouts
   - Add descriptive error messages
   - Implement proper retry strategies
   - Log relevant context on failure
   - Take screenshots on failure

## Example Usage

1. **Single API Call**:
   ```typescript
   When("I submit the form", async function(this: ScenarioWorld) {
       await pageObjects.FormPage.submitForm();
       this.response = await pageObjects.BasePage.waitForResponse('/api/submit', 'POST');
       expect(this.response.status).toBe("success");
   });
   ```

2. **Multiple API Calls**:
   ```typescript
   When("I load the dashboard", async function(this: ScenarioWorld) {
       const userPromise = pageObjects.BasePage.getResponsePromise('/api/user', 'GET');
       const dataPromise = pageObjects.BasePage.getResponsePromise('/api/data', 'GET');
       
       await pageObjects.DashboardPage.navigate();
       
       this.responses = {
           user: await (await userPromise).json(),
           data: await (await dataPromise).json()
       };
   });
   ```

3. **Form Handling**:
   ```typescript
   When("I fill the registration form", async function(this: ScenarioWorld, dataTable) {
       this.formData = dataTable.hashes()[0];
       await pageObjects.RegisterPage.fillForm(this.formData);
       
       const responsePromise = pageObjects.BasePage.getResponsePromise('/api/register', 'POST');
       await pageObjects.RegisterPage.submit();
       this.registrationResponse = await responsePromise;
   });
   ```

## Required Methods in BasePage

```typescript
class BasePage {
    async waitForResponse(url: string, method: string, timeout?: number): Promise<any>;
    async waitForElement(selector: string, timeout?: number): Promise<void>;
    async click(selector: string): Promise<void>;
    async fill(selector: string, value: string): Promise<void>;
    async getText(selector: string): Promise<string>;
    async isVisible(selector: string): Promise<boolean>;
    async waitForPageLoad(): Promise<void>;
}
```

## Test Requirements

1. Use Playwright's built-in assertions and fixtures
2. Implement proper waiting strategies
3. Handle API response interception
4. Use strong TypeScript typing
5. Follow BDD principles with Cucumber
6. Implement proper cleanup
7. Add meaningful error messages
8. Take screenshots on failure
9. Log relevant debug information
10. Use environment variables for configuration