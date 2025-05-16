import {  Given, Then, When } from "@cucumber/cucumber";
import PageObjects from "../pages/pageobjects";
import { ScenarioWorld } from "../setup/world";


let pageObjects = new PageObjects

Given("I am on the registration page", async () => {
    await pageObjects.RegisterPage.goto("customer/account/create/");
})

When("I fill in the registration form with valid data", async function (this: ScenarioWorld, dataTable) {
    const data = dataTable.hashes()[0]; 
    this.data = data
    await pageObjects.RegisterPage.fillRegisterForm(data.firstname, data.lastname, data.email, data.password);
})

When("I submit the form", async () => {
    await pageObjects.RegisterPage.submitRegisterForm();
})

Then("I validate the registration", async function(this:ScenarioWorld)  {
    await pageObjects.RegisterPage.validateRegistration(this.data.firstname, this.data.lastname, this.data.email);
})
