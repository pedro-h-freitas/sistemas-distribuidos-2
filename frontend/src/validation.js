export const NAME_MAX_LENGTH = 100;

export function validateUser({ id, name, password, roles }) {
  const errors = {};
  const trimmedName = name.trim();
  const trimmedPassword = password.trim();
  const trimmedRoles = roles.map((role) => role.trim()).filter(Boolean);

  if (!Number.isInteger(id) || id <= 0) {
    errors.id = "Informe um ID inteiro maior que zero.";
  }
  if (!trimmedName) {
    errors.name = "O nome é obrigatório.";
  } else if (trimmedName.length > NAME_MAX_LENGTH) {
    errors.name = `O nome deve ter no máximo ${NAME_MAX_LENGTH} caracteres.`;
  }
  if (!trimmedPassword) {
    errors.password = "A senha é obrigatória.";
  }
  if (trimmedRoles.length === 0) {
    errors.roles = "Informe ao menos um papel.";
  }

  return {
    errors,
    values: {
      id,
      name: trimmedName,
      password: trimmedPassword,
      roles: trimmedRoles,
    },
  };
}
