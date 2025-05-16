import { Page } from "@playwright/test";

let page:Page


export class BasePage {
     static page: Page;

    constructor(){
        page = BasePage.page
    }
  
    async goto(url: string) {
        await page.goto(url, {timeout: 60000, waitUntil: 'domcontentloaded' });

    }

    async waitForResponse(url:string, method:string, timeout=60000){
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


}