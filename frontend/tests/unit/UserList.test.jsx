import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { UserList } from "../../src/components/UserList";

describe("UserList", () => {
  it("exibe uma mensagem quando não há usuários", () => {
    render(<UserList users={[]} />);
    expect(screen.getByText("Nenhum usuário cadastrado.")).toBeInTheDocument();
  });

  it("exibe ID, nome e papéis sem expor a senha", () => {
    const users = [
      {
        id: 1,
        name: "Ana Silva",
        password: "segredo",
        roles: ["admin", "reader"],
      },
      { id: 2, name: "Bia", password: "outra-senha", roles: [] },
    ];
    render(<UserList users={users} />);

    expect(screen.getAllByRole("listitem")).toHaveLength(2);
    expect(screen.getByText(/Ana Silva/)).toBeInTheDocument();
    expect(screen.getByText("Papéis: admin, reader")).toBeInTheDocument();
    expect(screen.getByText(/ID: 2/)).toBeInTheDocument();
    expect(screen.getByText("Papéis: Nenhum")).toBeInTheDocument();
    expect(screen.queryByText("segredo")).not.toBeInTheDocument();
    expect(screen.queryByText("outra-senha")).not.toBeInTheDocument();
  });
});
