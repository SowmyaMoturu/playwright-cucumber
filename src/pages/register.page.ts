import { BasePage } from "./basepage";

import { expect, Page } from "@playwright/test";

let page: Page

let locators = {
    "firstname" : "#firstname",
    "lastname" : "#lastname",
    "email" : "#email_address",
    "password" : "#password",
    "confirm_password" : "#password-confirmation",
    "submit" :"Create an Account",
    "successMessage" : ".message-success",
    "welcomeMessage" : ".box-information .box-content",
    "accountInfo" : ".box-information .box-content"
}

export class RegisterPage extends BasePage {
    
    constructor() {
        super();
        page = BasePage.page
    }

    async fillRegisterForm(firstname: string, lastname: string, email: string, password: string) {
        await page.fill(locators.firstname, firstname);
        await page.fill(locators.lastname, lastname);
        await page.fill(locators.email, email);
        await page.fill(locators.password, password);
        await page.fill(locators.confirm_password, password);
    }

    async submitRegisterForm() {
        await page.getByRole('button', { name: locators.submit }).click();
        await page.waitForLoadState('networkidle');
    }

    async validateRegistration(firstName: string, lastName: string, email: string) {
        const successMessage = await page.locator(locators.successMessage).textContent();
       
        // Validate the success message contains expected text
        expect(successMessage).toContain('Th you for registing');
  
        // Validate we're on the account page
        const currentUrl = page.url();
        console.log(`Current URL: ${currentUrl}`);
        expect(currentUrl).toContain('/customer/account/');
    
        // Validate welcome message contains the user's name
        const welcomeMessage = await page.locator(locators.welcomeMessage).textContent();
        expect(welcomeMessage).toContain(firstName);
        expect(welcomeMessage).toContain(lastName);
    
        // Validate the email in the account information
        const accountInfo = await page.locator(locators.accountInfo).textContent();
        expect(accountInfo).toContain(email);
    }


}