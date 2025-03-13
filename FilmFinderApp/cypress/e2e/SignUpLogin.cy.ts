describe("Sign-up and Log-in", () => {
  const username = "testuser7@gmail.com";
  const password = "1234567";
  it("Can Sign-up", () => {
    cy.visit("/login");
    cy.get("button").contains("Sign-up Here").click();
    cy.contains("h2", "Create a Profile").should("be.visible");
    cy.get("input[name='username']").type(username);
    cy.get("input[name='password']").type(password);
    cy.contains("button", "Save").should("be.visible").click();
    cy.wait(3000);
  });
  it("Can Log-in and Interact", () => {
    cy.visit("/login");
    cy.contains("h2", "Sign in to your account").should("be.visible");
    cy.get("input[name='email']").type("testuser7@gmail.com");
    cy.get("input[name='password']").type(password);
    cy.contains("button", "Sign in").should("be.visible").click();
    cy.wait(3000);
    cy.contains("a", "Finder").should("be.visible");
    cy.contains("a", "watchList").should("be.visible");
    cy.get("#info_button").should("exist").click();
    cy.contains("dt", "Language").should("exist");
    cy.get("#info_button").should("exist").click();
    cy.get("#liked").should("exist").click();
    cy.wait(1000);
    cy.get("#not_watched").should("exist").click();
    cy.wait(1000);
    cy.get("#watch_later").should("exist").click();
    cy.wait(1000);
    cy.get("#disliked").should("exist").click();
    cy.wait(1000);
    cy.contains("a", "watchList").should("be.visible").click();
    cy.get("#info_button").should("exist").click();
    cy.get("#account_button").should("exist").click();
    cy.contains("a", "Sign out").should("be.visible").click();
    cy.contains("h2", "Sign in to your account").should("be.visible");
  });

  after(() => {
    cy.wait(3000);
    cy.request({
      method: "DELETE",
      url: "http://127.0.0.1:8000/api/user/delete/",
      body: { username: username },
      headers: {
        "Content-Type": "application/json", // Ensure correct header
      },
    }).then((response) => {
      expect(response.status).to.eq(200);
    });
  });
});
