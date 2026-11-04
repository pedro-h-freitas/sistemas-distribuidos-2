import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it, vi } from "vitest";
import { UserForm } from "../../src/components/UserForm";

describe("UserForm", () => {
  it("renderiza os campos do usuário e o botão", () => {
    render(<UserForm onAdd={() => {}} />);

    expect(screen.getByLabelText("ID")).toBeInTheDocument();
    expect(screen.getByLabelText("Nome")).toBeInTheDocument();
    expect(screen.getByLabelText("Senha")).toHaveAttribute("type", "password");
    expect(screen.getByLabelText("Papéis")).toBeInTheDocument();
    expect(
      screen.getByRole("button", { name: "Adicionar usuário" }),
    ).toBeInTheDocument();
  });

  it("envia os valores normalizados e limpa o formulário", async () => {
    const user = userEvent.setup();
    const onAdd = vi.fn();
    render(<UserForm onAdd={onAdd} />);

    await user.type(screen.getByLabelText("ID"), "42");
    await user.type(screen.getByLabelText("Nome"), "  Ana Silva  ");
    await user.type(screen.getByLabelText("Senha"), "  segredo  ");
    await user.type(screen.getByLabelText("Papéis"), "admin, reader");
    await user.click(screen.getByRole("button", { name: "Adicionar usuário" }));

    expect(onAdd).toHaveBeenCalledWith({
      id: 42,
      name: "Ana Silva",
      password: "segredo",
      roles: ["admin", "reader"],
    });
    expect(screen.getByLabelText("ID")).toHaveValue(null);
    expect(screen.getByLabelText("Nome")).toHaveValue("");
    expect(screen.getByLabelText("Senha")).toHaveValue("");
    expect(screen.getByLabelText("Papéis")).toHaveValue("");
  });

  it("não envia dados inválidos e mostra os erros", async () => {
    const user = userEvent.setup();
    const onAdd = vi.fn();
    render(<UserForm onAdd={onAdd} />);

    await user.click(screen.getByRole("button", { name: "Adicionar usuário" }));

    expect(screen.getAllByRole("alert")).toHaveLength(4);
    expect(onAdd).not.toHaveBeenCalled();
  });
});
