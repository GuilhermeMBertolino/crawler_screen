/// <reference types="cypress" />

it("Tenda search", () => { 
    // Select routers option
    cy.visit("https://www.tendacn.com/br/download/default.html")
    cy.get(':nth-child(3) > :nth-child(1) > .col3mlr > .select2 > .selection > .select2-selection > .select2-selection__arrow')
        .click()
    cy.get('.select2-search__field')
        .click()
        .type("Roteadores{enter}")

    // Select first option router
    cy.get(':nth-child(2) > .col3mlr > .select2 > .selection > .select2-selection > .select2-selection__arrow')
        .click()
    cy.get('.select2-search__field')
        .click()
        .type("Wi-Fi 7 Routers{enter}")
})