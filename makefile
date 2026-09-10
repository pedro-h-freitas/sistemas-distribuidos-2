.PHONY: help install test lint format run \
        up up-build down stop build logs ps shell-api

PYTEST := poetry run pytest
UVICORN := poetry run uvicorn
RUFF := poetry run ruff

PORT := 8000
COMPOSE := docker compose
BACKEND := backend


help:
	@echo "Comandos disponíveis:"
	@echo ""
	@echo "  Comandos Python/Poetry"
	@echo "    make install                    - instala as dependências"
	@echo "    make test                       - executa os testes"
	@echo "    make lint                       - verifica problemas no código"
	@echo "    make format                     - formata o código"
	@echo "    make run                        - inicia o servidor FastAPI"
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
	cd $(BACKEND) && poetry install

test:
	cd $(BACKEND) && $(PYTEST)

lint:
	cd $(BACKEND) && $(RUFF) check .

format:
	cd $(BACKEND) && $(RUFF) format .

run:
	cd $(BACKEND) && $(UVICORN) app.main:app --reload --port $(PORT)

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
