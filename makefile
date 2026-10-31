.PHONY: help install test test-verbose lint format format-check run \
        alembic-create alembic-check alembic-history alembic-upgrade-head alembic-downgrade \
        up up-build down stop build logs ps shell-api

CD_BACKEND := cd backend

PYTEST := $(CD_BACKEND) && poetry run pytest
UVICORN := $(CD_BACKEND) && poetry run uvicorn
RUFF := $(CD_BACKEND) && poetry run ruff
ALEMBIC := $(CD_BACKEND) && poetry run alembic

PORT := 8000
COMPOSE := docker compose
BACKEND := backend


help:
	@echo "Comandos disponíveis:"
	@echo ""
	@echo "  Comandos Python/Poetry"
	@echo "    make install                    - instala as dependências"
	@echo "    make test                       - executa os testes"
	@echo "    make test-verbose               - executa os testes com a flag verbose"
	@echo "    make lint                       - verifica problemas no código"
	@echo "    make format                     - formata o código"
	@echo "    make format-check               - verifica a formatação do código"
	@echo "    make run                        - inicia o servidor FastAPI"
	@echo ""
	@echo "  Comandos Alembic"
	@echo "    make alembic-create MESSAGE=<message>  - Cria uma nova migration"
	@echo "    make alembic-check                     - Checa se as models criadas estão corretas"
	@echo "    make alembic-current                   - Mostra o estado atual das migrations"
	@echo "    make alembic-history                   - Mostra o historico das migrations"
	@echo "    make alembic-upgrade-head              - Executa as migrations para o head do hisotry"
	@echo "    make alembic-downgrade                 - Reverte a última migration"
	@echo ""
	@echo "  Comandos Docker"
	@echo "    make ps                         - lista os containers"
	@echo "    make build                      - builda a imagem dos serviços"
	@echo "    make build SERVICE=<service>    - builda a imagem do serviço (ex.: api, db)"
	@echo "    make up                         - inicia todos os serviços"
	@echo "    make up SERVICE=<service>       - inicia o serviço (ex.: api, db)"
	@echo "    make up-build                   - builda e inicia todos os serviços"
	@echo "    make up-build SERVICE=<service> - builda e inicia o serviço (ex.: api, db)"
	@echo "    make stop SERVICE=<service>     - para um serviço (ex.: api, db)"
	@echo "    make down                       - para e remove todos os containers"
	@echo "    make logs SERVICE=<service>     - acompanha os logs do serviço (ex.: api, db)"
	@echo "    make shell-api                  - abre um shell no container da API"


install:
	$(CD_BACKEND) && poetry install

test:
	$(PYTEST)

test-verbose:
	$(PYTEST) -v

lint:
	$(RUFF) check .

format:
	$(RUFF) format .

format-check:
	$(RUFF) format --check .

run:
	$(UVICORN) app.main:app --reload --port $(PORT)

alembic-create:
	$(ALEMBIC) revision --autogenerate -m "$(MESSAGE)"

alembic-check:
	$(ALEMBIC) check

alembic-current:
	$(ALEMBIC) current

alembic-history:
	$(ALEMBIC) history

alembic-upgrade-head:
	$(ALEMBIC) upgrade head

alembic-downgrade:
	$(ALEMBIC) downgrade -1

up:
	$(COMPOSE) up -d $(SERVICE)

up-build:
	$(COMPOSE) up -d --build $(SERVICE)

stop:
	$(COMPOSE) stop $(SERVICE)

down:
	$(COMPOSE) down

build:
	$(COMPOSE) build $(SERVICE)

logs:
	$(COMPOSE) logs -f $(SERVICE)

ps:
	$(COMPOSE) ps

shell-api:
	$(COMPOSE) exec api sh
