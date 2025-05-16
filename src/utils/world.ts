import { setWorldConstructor } from '@cucumber/cucumber';
import { Page, Response } from '@playwright/test';

export class CustomWorld {
    page!: Page;
    context: any;
    testName: string;
    responseData: Map<string, any>;
    
    constructor() {
        this.context = {};
        this.responseData = new Map();
        this.testName = '';
    }

    setPage(page: Page) {
        this.page = page;
    }

    async saveResponse(key: string, response: Response) {
        try {
            const data = await response.json();
            this.responseData.set(key, data);
        } catch (error) {
            console.error(`Failed to parse response for key ${key}:`, error);
            this.responseData.set(key, null);
        }
    }

    getResponseData(key: string) {
        return this.responseData.get(key);
    }
}

setWorldConstructor(CustomWorld); 