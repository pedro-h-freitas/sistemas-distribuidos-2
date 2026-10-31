# sistemas-distribuidos-2
Repositório para a disciplina de Sistemas Distribuídos - 2026.2

## Backend

Os comandos do projeto estão disponíveis em `makefile` e executam as tarefas do backend dentro de `backend/`.

### Testes

Para executar toda a suíte de testes a partir da raiz do repositório, use:

```bash
make test
```

Os testes usam o PostgreSQL configurado em `TEST_DATABASE_URL` (por padrão,
`db_example_test`). Crie esse banco uma vez antes de executar a suíte:

```bash
docker compose up -d db
docker compose exec db createdb -U ${POSTGRES_USER} ${POSTGRES_TEST_DB}
```

Para visualizar informações detalhadas sobre cada teste durante a execução, use:

```bash
make test-verbose
```

Também é possível executar os testes diretamente no diretório do backend:

```bash
cd backend
poetry run pytest
```
