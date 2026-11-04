import { describe, expect, it } from "vitest";
import { NAME_MAX_LENGTH, validateUser } from "../../src/validation";

const validUser = {
  id: 1,
  name: "Ana Silva",
  password: "segredo",
  roles: ["admin", "reader"],
};

describe("validateUser", () => {
  it("aceita e normaliza dados válidos", () => {
    const { errors, values } = validateUser({
      ...validUser,
      name: "  Ana Silva  ",
      password: " segredo ",
      roles: [" admin ", "", " reader "],
    });

    expect(errors).toEqual({});
    expect(values).toEqual(validUser);
  });

  it.each([0, -1, 1.5, Number.NaN])("rejeita ID inválido: %s", (id) => {
    const { errors } = validateUser({ ...validUser, id });
    expect(errors.id).toBeDefined();
  });

  it("rejeita nome vazio ou com mais de 100 caracteres", () => {
    expect(
      validateUser({ ...validUser, name: "   " }).errors.name,
    ).toBeDefined();
    expect(
      validateUser({ ...validUser, name: "a".repeat(NAME_MAX_LENGTH + 1) })
        .errors.name,
    ).toBeDefined();
  });

  it("rejeita senha vazia e lista sem papéis válidos", () => {
    const { errors } = validateUser({
      ...validUser,
      password: "  ",
      roles: ["", "  "],
    });

    expect(errors.password).toBeDefined();
    expect(errors.roles).toBeDefined();
  });
});
