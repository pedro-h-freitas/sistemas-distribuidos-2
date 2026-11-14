import { useEffect, useState } from "react";
import { UserForm } from "./components/UserForm";
import { UserList } from "./components/UserList";
import { createUser, listUsers } from "./services/user";

export default function App() {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [loadError, setLoadError] = useState("");

  useEffect(() => {
    listUsers()
      .then(setUsers)
      .catch((error) => setLoadError(error.message))
      .finally(() => setLoading(false));
  }, []);

  async function addUser(user) {
    const created = await createUser(user); // lança erro se falhar
    setUsers((current) => [...current, created]);
  }

  return (
    <main className="mx-auto min-h-screen max-w-xl space-y-6 p-4 sm:p-6">
      <h1 className="text-3xl font-bold">Gerenciador de Usuários</h1>
      <UserForm onAdd={addUser} />
      <section aria-labelledby="users-heading" className="space-y-3">
        <h2 id="users-heading" className="text-xl font-semibold">
          Usuários cadastrados
        </h2>
        <UserList
          users={users}
          loading={loading}
          loadError={loadError}
        />
      </section>
    </main>
  );
}
