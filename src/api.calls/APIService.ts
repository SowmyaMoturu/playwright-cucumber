
import { APIRequestContext, APIRequest, APIResponse } from "@playwright/test";

let request: APIRequestContext;
let country: string

export class APIService {
    constructor(){

    }
    async getJsonResponse(response: APIResponse) {
        if (!response.ok()) {
            throw new Error(`Request failed with status ${response.status()}: ${response.statusText()}`);
        }
        let jsonResponse = await response.json();
        return jsonResponse;
    }
}