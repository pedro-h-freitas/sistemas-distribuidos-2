# sistemas-distribuidos-2
Repositório para a disciplina de Sistemas Distribuídos - 2026.2

## Backend

Os comandos do projeto estão disponíveis em `makefile` e executam as tarefas do backend dentro de `backend/`.

### Testes

Para executar toda a suíte de testes a partir da raiz do repositório, use:

```bash
make test
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
