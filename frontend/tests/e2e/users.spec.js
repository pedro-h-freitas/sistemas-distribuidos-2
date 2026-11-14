import { expect, test } from "@playwright/test";

// Isola os cenários de UI que exigem uma lista vazia, sem apagar registros do banco.
async function mockEmptyUsers(page) {
  await page.route("**/users", async (route) => {
    if (route.request().method() === "GET") {
      await route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify([]),
      });
    } else {
      await route.continue();
    }
  });
}

test("mostra a lista vazia de usuários", async ({ page }) => {
  await mockEmptyUsers(page);
  await page.goto("/");

  await expect(page.getByText("Nenhum usuário cadastrado.")).toBeVisible();
});

test("persiste o usuário no backend após page.reload()", async ({ page, request }) => {
  // ID exclusivo para não depender dos registros já existentes no banco.
  const userId = 1_000_000_000 + Math.floor(Math.random() * 1_000_000_000);
  const name = `Ana Silva E2E ${userId}`;
  const password = "segredo-e2e";
  let createdUserUrl;

  try {
    await page.goto("/");
    await expect(page.getByRole("heading", { name: "Gerenciador de Usuários" })).toBeVisible();

    await page.getByLabel("ID").fill(String(userId));
    await page.getByLabel("Nome").fill(name);
    await page.getByLabel("Senha").fill(password);
    await page.getByLabel("Papéis").fill("admin, reader");

    const postResponsePromise = page.waitForResponse(
      (response) =>
        new URL(response.url()).pathname === "/users" &&
        response.request().method() === "POST",
    );
    await page.getByRole("button", { name: "Adicionar usuário" }).click();
    const postResponse = await postResponsePromise;
    expect(postResponse.status()).toBe(201);
    createdUserUrl = `${postResponse.url()}/${userId}`;

    const userItem = page.getByRole("listitem").filter({ hasText: name });
    await expect(userItem).toContainText(`(ID: ${userId})`);
    await expect(userItem).toContainText("Papéis: admin, reader");
    await expect(page.getByText(password)).toBeHidden();

    // O reload desmonta o React e força uma nova leitura GET /users.
    const getResponsePromise = page.waitForResponse(
      (response) =>
        new URL(response.url()).pathname === "/users" &&
        response.request().method() === "GET",
    );
    await page.reload();
    const getResponse = await getResponsePromise;
    expect(getResponse.ok()).toBeTruthy();

    const persistedUsers = await getResponse.json();
    expect(persistedUsers).toEqual(
      expect.arrayContaining([
        expect.objectContaining({
          id: userId,
          name,
          roles: ["admin", "reader"],
        }),
      ]),
    );
    await expect(page.getByRole("listitem").filter({ hasText: name })).toContainText(
      "Papéis: admin, reader",
    );
    await expect(page.getByText(password)).toBeHidden();
  } finally {
    // Remove apenas o registro criado pelo teste, mesmo em caso de falha de assertiva.
    if (createdUserUrl) {
      const deleteResponse = await request.delete(createdUserUrl);
      expect(deleteResponse.status()).toBe(204);
    }
  }
});

test("não cadastra usuário com dados inválidos", async ({ page }) => {
  await mockEmptyUsers(page);
  await page.goto("/");

  await page.getByRole("button", { name: "Adicionar usuário" }).click();

  await expect(page.getByRole("alert")).toHaveCount(4);
  await expect(page.getByText("Nenhum usuário cadastrado.")).toBeVisible();
});
