import { setWorldConstructor, World, IWorldOptions } from '@cucumber/cucumber';
import * as messages from '@cucumber/messages';
import { BrowserContext, Page, PlaywrightTestOptions, APIRequestContext, Response } from '@playwright/test';


export interface ScenarioWorld extends World {
    data?: any;
    debug: boolean;
    feature?: messages.Pickle;
    context?: BrowserContext;
    page?: Page;

    testName?: string;
    startTime?: Date;

    request?: APIRequestContext;
    baseUrl?: string;
    apiUrl?: string;
    username?: string;
    playwrightOptions?: PlaywrightTestOptions;
    
    // Response handling
    responseData: Map<string, any>;
    saveResponse(key: string, response: Response): Promise<void>;
    getResponseData(key: string): any;
}

export class CustomWorld extends World implements ScenarioWorld {
    debug = false;
    responseData: Map<string, any>;

    constructor(options: IWorldOptions) {
        super(options);
        this.responseData = new Map();
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