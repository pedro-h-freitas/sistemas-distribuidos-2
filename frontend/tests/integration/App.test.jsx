import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import App from "../../src/App";

const ana = { id: 1, name: "Ana", roles: ["admin", "reader"] };

function jsonResponse(data, status = 200) {
  return {
    ok: status >= 200 && status < 300,
    status,
    json: async () => data,
  };
}

function deferred() {
  let resolve;
  let reject;
  const promise = new Promise((res, rej) => {
    resolve = res;
    reject = rej;
  });
  return { promise, resolve, reject };
}

beforeEach(() => {
  vi.stubGlobal("fetch", vi.fn());
});

afterEach(() => {
  vi.unstubAllGlobals();
});

describe("App: integração com API de usuários", () => {
  it("exibe carregamento enquanto o fetch está pendente", async () => {
    const pending = deferred();
    fetch.mockReturnValueOnce(pending.promise);

    render(<App />);

    expect(screen.getByText("Carregando usuários.")).toBeInTheDocument();
    expect(fetch).toHaveBeenCalledWith(
      expect.stringMatching(/\/users$/),
      expect.objectContaining({ method: "GET" }),
    );

    pending.resolve(jsonResponse([]));
    expect(await screen.findByText("Nenhum usuário cadastrado.")).toBeInTheDocument();
    expect(screen.queryByText("Carregando usuários.")).not.toBeInTheDocument();
  });

  it("renderiza usuários retornados pelo fetch", async () => {
    fetch.mockResolvedValueOnce(jsonResponse([ana]));

    render(<App />);

    expect(await screen.findByText(/Ana/)).toBeInTheDocument();
    expect(screen.getByText("Papéis: admin, reader")).toBeInTheDocument();
    expect(screen.queryByText("Nenhum usuário cadastrado.")).not.toBeInTheDocument();
  });

  it("mostra lista vazia quando a API retorna []", async () => {
    fetch.mockResolvedValueOnce(jsonResponse([]));

    render(<App />);

    expect(await screen.findByText("Nenhum usuário cadastrado.")).toBeInTheDocument();
  });

  it("exibe o detalhe do erro HTTP retornado pela API", async () => {
    fetch.mockResolvedValueOnce(jsonResponse({ detail: "Serviço indisponível" }, 503));

    render(<App />);

    expect(await screen.findByText(/Erro ao carregar usuários: Serviço indisponível/)).toBeInTheDocument();
    expect(screen.queryByText("Nenhum usuário cadastrado.")).not.toBeInTheDocument();
  });

  it("exibe erro de rede quando o fetch rejeita", async () => {
    fetch.mockRejectedValueOnce(new Error("Falha de conexão"));

    render(<App />);

    expect(await screen.findByText(/Erro ao carregar usuários: Falha de conexão/)).toBeInTheDocument();
  });

  it("cadastra usuário via POST e atualiza a lista com a resposta da API", async () => {
    const user = userEvent.setup();
    fetch
      .mockResolvedValueOnce(jsonResponse([]))
      .mockResolvedValueOnce(jsonResponse(ana, 201));

    render(<App />);
    expect(await screen.findByText("Nenhum usuário cadastrado.")).toBeInTheDocument();

    await user.type(screen.getByLabelText("ID"), "1");
    await user.type(screen.getByLabelText("Nome"), "Ana");
    await user.type(screen.getByLabelText("Senha"), "segredo");
    await user.type(screen.getByLabelText("Papéis"), "admin, reader");
    await user.click(screen.getByRole("button", { name: "Adicionar usuário" }));

    expect(await screen.findByText("Papéis: admin, reader")).toBeInTheDocument();
    expect(fetch).toHaveBeenCalledTimes(2);
    expect(fetch).toHaveBeenNthCalledWith(
      2,
      expect.stringMatching(/\/users$/),
      expect.objectContaining({
        method: "POST",
        body: JSON.stringify({
          id: 1,
          name: "Ana",
          password: "segredo",
          roles: ["admin", "reader"],
        }),
      }),
    );
    expect(screen.queryByText("segredo")).not.toBeInTheDocument();
  });
});
