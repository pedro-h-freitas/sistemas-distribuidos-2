.PHONY: help front-install front-dev front-lint front-format front-check front-test front-test-e2e front-build \
        back-install back-test back-test-verbose back-lint back-format back-format-check back-run \
        alembic-create alembic-check alembic-current alembic-history alembic-upgrade-head alembic-downgrade \
        docker-up docker-up-build docker-stop docker-down docker-build docker-logs docker-ps docker-shell-api

CD_BACKEND := cd backend

NPM := npm --prefix frontend

PYTEST := $(CD_BACKEND) && poetry run pytest
UVICORN := $(CD_BACKEND) && poetry run uvicorn
RUFF := $(CD_BACKEND) && poetry run ruff
ALEMBIC := $(CD_BACKEND) && poetry run alembic

PORT := 8000
COMPOSE := docker compose


help:
	@echo "Comandos disponíveis:"
	@echo ""
	@echo "  Comandos Frontend/npm"
	@echo "    make front-install                   - instala dependências pelo lockfile"
	@echo "    make front-dev                       - inicia o servidor de desenvolvimento Vite"
	@echo "    make front-lint                      - verifica problemas com o Biome"
	@echo "    make front-format                    - formata os arquivos com o Biome"
	@echo "    make front-check                     - executa as verificações do Biome"
	@echo "    make front-test                      - executa os testes unitários e de integração"
	@echo "    make front-test-e2e                  - executa os testes E2E com Playwright"
	@echo "    make front-build                     - gera a versão de produção do frontend"
	@echo ""
	@echo "  Comandos Python/Poetry"
	@echo "    make back-install                         - instala as dependências Python"
	@echo "    make back-test                            - executa os testes do backend"
	@echo "    make back-test-verbose                    - executa os testes com saída detalhada"
	@echo "    make back-lint                            - verifica problemas no código Python"
	@echo "    make back-format                          - formata o código Python"
	@echo "    make back-format-check                    - verifica a formatação do código Python"
	@echo "    make back-run                             - inicia o servidor FastAPI"
	@echo ""
	@echo "  Comandos Alembic"
	@echo "    make alembic-create MESSAGE=<message>  - Cria uma nova migration"
	@echo "    make alembic-check                     - verifica se os models estão sincronizados"
	@echo "    make alembic-current                   - mostra a revisão aplicada no banco"
	@echo "    make alembic-history                   - mostra o histórico de migrations"
	@echo "    make alembic-upgrade-head              - aplica migrations até a revisão mais recente"
	@echo "    make alembic-downgrade                 - reverte a última migration"
	@echo ""
	@echo "  Comandos Docker"
	@echo "    make docker-ps                         - lista os containers ativos"
	@echo "    make docker-build [SERVICE=<service>]  - constrói todas as imagens ou a imagem do serviço"
	@echo "    make docker-up [SERVICE=<service>]     - inicia todos os serviços ou um serviço"
	@echo "    make docker-up-build [SERVICE=<service>] - constrói e inicia todos ou um serviço"
	@echo "    make docker-stop SERVICE=<service>     - para o serviço"
	@echo "    make docker-down                       - para e remove os containers"
	@echo "    make docker-logs SERVICE=<service>     - acompanha os logs do serviço"
	@echo "    make docker-shell-api                  - abre um shell no container da API"


front-install:
	$(NPM) ci

front-dev:
	$(NPM) run dev

front-lint:
	$(NPM) run lint

front-format:
	$(NPM) run format

front-check:
	$(NPM) run check

front-test:
	$(NPM) run test

front-test-e2e:
	$(NPM) run test:e2e

front-build:
	$(NPM) run build

back-install:
	$(CD_BACKEND) && poetry install

back-test:
	$(PYTEST)

back-test-verbose:
	$(PYTEST) -v

back-lint:
	$(RUFF) check .

back-format:
	$(RUFF) format .

back-format-check:
	$(RUFF) format --check .

back-run:
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

docker-up:
	$(COMPOSE) up -d $(SERVICE)

docker-up-build:
	$(COMPOSE) up -d --build $(SERVICE)

docker-stop:
	$(COMPOSE) stop $(SERVICE)

docker-down:
	$(COMPOSE) down

docker-build:
	$(COMPOSE) build $(SERVICE)

docker-logs:
	$(COMPOSE) logs -f $(SERVICE)

docker-ps:
	$(COMPOSE) ps

docker-shell-api:
	$(COMPOSE) exec api sh
