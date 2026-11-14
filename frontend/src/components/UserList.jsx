export function UserList({ users, loading, loadError }) {
  if (loading) {
    return <p className="text-slate-600">Carregando usuários.</p>;
  }

  if (loadError) {
    return <p role="alert" className="text-slate-600">Erro ao carregar usuários: {loadError}.</p>;
  }

  if (users.length === 0) {
    return <p className="text-slate-600">Nenhum usuário cadastrado.</p>;
  }

  return (
    <ul className="space-y-2">
      {users.map((user) => (
        <li
          key={user.id}
          className="rounded-lg border border-slate-200 bg-white p-4 shadow-sm"
        >
          <p className="font-medium">
            {user.name}{" "}
            <span className="text-sm text-slate-600">(ID: {user.id})</span>
          </p>
          <p className="text-sm text-slate-600">
            Papéis: {user.roles.length > 0 ? user.roles.join(", ") : "Nenhum"}
          </p>
        </li>
      ))}
    </ul>
  );
}
