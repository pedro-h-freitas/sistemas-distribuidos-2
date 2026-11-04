import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it } from "vitest";
import App from "../../src/App";

describe("fluxo local de usuários", () => {
  it("começa com a lista vazia", () => {
    render(<App />);
    expect(screen.getByText("Nenhum usuário cadastrado.")).toBeInTheDocument();
  });

  it("cadastra usuários e atualiza a lista", async () => {
    const user = userEvent.setup();
    render(<App />);

    await user.type(screen.getByLabelText("ID"), "1");
    await user.type(screen.getByLabelText("Nome"), "Ana");
    await user.type(screen.getByLabelText("Senha"), "segredo");
    await user.type(screen.getByLabelText("Papéis"), "admin, reader");
    await user.click(screen.getByRole("button", { name: "Adicionar usuário" }));

    expect(screen.getByText(/Ana/)).toBeInTheDocument();
    expect(screen.getByText("Papéis: admin, reader")).toBeInTheDocument();
    expect(
      screen.queryByText("Nenhum usuário cadastrado."),
    ).not.toBeInTheDocument();
    expect(screen.queryByText("segredo")).not.toBeInTheDocument();
  });
});
