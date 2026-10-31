import { expect, test } from "@playwright/test";

test("mostra a lista vazia de usuários", async ({ page }) => {
  await page.goto("/");

  await expect(page.getByText("Nenhum usuário cadastrado.")).toBeVisible();
});

test("cadastra um usuário e exibe seus dados sem a senha", async ({ page }) => {
  await page.goto("/");

  await page.getByLabel("ID").fill("1");
  await page.getByLabel("Nome").fill("Ana Silva");
  await page.getByLabel("Senha").fill("segredo");
  await page.getByLabel("Papéis").fill("admin, reader");
  await page.getByRole("button", { name: "Adicionar usuário" }).click();

  await expect(page.getByRole("listitem")).toContainText("Ana Silva");
  await expect(page.getByRole("listitem")).toContainText(
    "Papéis: admin, reader",
  );
  await expect(page.getByText("Nenhum usuário cadastrado.")).toBeHidden();
  await expect(page.getByText("segredo")).toBeHidden();
});

test("não cadastra usuário com dados inválidos", async ({ page }) => {
  await page.goto("/");

  await page.getByRole("button", { name: "Adicionar usuário" }).click();

  await expect(page.getByRole("alert")).toHaveCount(4);
  await expect(page.getByText("Nenhum usuário cadastrado.")).toBeVisible();
});
