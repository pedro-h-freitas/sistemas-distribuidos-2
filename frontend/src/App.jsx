import { useState } from "react";
import { UserForm } from "./components/UserForm";
import { UserList } from "./components/UserList";

export default function App() {
  const [users, setUsers] = useState([]);

  function addUser(user) {
    setUsers((current) => [...current, user]);
  }

  return (
    <main className="mx-auto min-h-screen max-w-xl space-y-6 p-4 sm:p-6">
      <h1 className="text-3xl font-bold">Gerenciador de Usuários</h1>
      <UserForm onAdd={addUser} />
      <section aria-labelledby="users-heading" className="space-y-3">
        <h2 id="users-heading" className="text-xl font-semibold">
          Usuários cadastrados
        </h2>
        <UserList users={users} />
      </section>
    </main>
  );
}
