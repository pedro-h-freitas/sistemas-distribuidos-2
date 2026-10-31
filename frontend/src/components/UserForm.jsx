import { useState } from "react";
import { validateUser } from "../validation";

export function UserForm({ onAdd }) {
  const [id, setId] = useState("");
  const [name, setName] = useState("");
  const [password, setPassword] = useState("");
  const [roles, setRoles] = useState("");
  const [errors, setErrors] = useState({});

  function handleSubmit(event) {
    event.preventDefault();
    const result = validateUser({
      id: Number(id),
      name,
      password,
      roles: roles.split(","),
    });
    setErrors(result.errors);
    if (Object.keys(result.errors).length > 0) return;

    onAdd(result.values);
    setId("");
    setName("");
    setPassword("");
    setRoles("");
  }

  return (
    <form
      onSubmit={handleSubmit}
      noValidate
      className="space-y-4 rounded-lg border border-slate-200 bg-white p-4 shadow-sm"
    >
      <div className="space-y-1">
        <label htmlFor="user-id" className="block text-sm font-medium">
          ID
        </label>
        <input
          id="user-id"
          type="number"
          min="1"
          step="1"
          value={id}
          onChange={(event) => setId(event.target.value)}
          aria-invalid={errors.id ? "true" : "false"}
          aria-describedby={errors.id ? "user-id-error" : undefined}
          className="w-full rounded border border-slate-300 p-2"
        />
        {errors.id && (
          <p id="user-id-error" role="alert" className="text-sm text-red-700">
            {errors.id}
          </p>
        )}
      </div>

      <div className="space-y-1">
        <label htmlFor="user-name" className="block text-sm font-medium">
          Nome
        </label>
        <input
          id="user-name"
          value={name}
          onChange={(event) => setName(event.target.value)}
          aria-invalid={errors.name ? "true" : "false"}
          aria-describedby={errors.name ? "user-name-error" : undefined}
          placeholder="Ex.: Ana Silva"
          className="w-full rounded border border-slate-300 p-2"
        />
        {errors.name && (
          <p id="user-name-error" role="alert" className="text-sm text-red-700">
            {errors.name}
          </p>
        )}
      </div>

      <div className="space-y-1">
        <label htmlFor="user-password" className="block text-sm font-medium">
          Senha
        </label>
        <input
          id="user-password"
          type="password"
          value={password}
          onChange={(event) => setPassword(event.target.value)}
          aria-invalid={errors.password ? "true" : "false"}
          aria-describedby={errors.password ? "user-password-error" : undefined}
          autoComplete="new-password"
          className="w-full rounded border border-slate-300 p-2"
        />
        {errors.password && (
          <p
            id="user-password-error"
            role="alert"
            className="text-sm text-red-700"
          >
            {errors.password}
          </p>
        )}
      </div>

      <div className="space-y-1">
        <label htmlFor="user-roles" className="block text-sm font-medium">
          Papéis
        </label>
        <input
          id="user-roles"
          value={roles}
          onChange={(event) => setRoles(event.target.value)}
          aria-invalid={errors.roles ? "true" : "false"}
          aria-describedby={
            errors.roles ? "user-roles-error" : "user-roles-help"
          }
          placeholder="Ex.: admin, reader"
          className="w-full rounded border border-slate-300 p-2"
        />
        <p id="user-roles-help" className="text-sm text-slate-600">
          Separe os papéis por vírgula.
        </p>
        {errors.roles && (
          <p
            id="user-roles-error"
            role="alert"
            className="text-sm text-red-700"
          >
            {errors.roles}
          </p>
        )}
      </div>

      <button
        type="submit"
        className="w-full rounded bg-blue-600 px-4 py-2 font-medium text-white hover:bg-blue-700 sm:w-auto"
      >
        Adicionar usuário
      </button>
    </form>
  );
}
