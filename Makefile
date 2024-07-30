.PHONY: build run stop ps host

OMIT_PATHS := "*/__init__.py,backend/tests/*"

define PRINT_HELP_PYSCRIPT
import re, sys

regex_pattern = r'^([a-zA-Z_-]+):.*?## (.*)$$'

for line in sys.stdin:
	match = re.match(regex_pattern, line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

# Loads environment variable
include .env

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

clean-logs: # Removes log info. Usage: make clean-logs
	rm -fr dist/ .eggs/
	find . -name '*.log' -o -name '*.log' -exec rm -fr {} +

clean-test: # Remove test and coverage artifacts
	rm -fr .tox/ .testmondata* .coverage coverage.* htmlcov/ .pytest_cache

clean-cache: # remove test and coverage artifacts
	find . -name '*pycache*' -exec rm -rf {} +

clean: clean-logs clean-test clean-cache ## Add a rule to remove unnecessary assets. Usage: make clean

sanitize: # Remove dangling images and volumes
	docker system prune --volumes -f
	docker images --filter 'dangling=true' -q --no-trunc | xargs -r docker rmi

env: ## Creates a virtual environment. Usage: make env
	pip install virtualenv
	virtualenv .venv

install: ## Installs the python requirements. Usage: make install
	pip install uv
	uv pip install -r requirements.txt
	uv pip install -r requirements-dev.txt

run: ## Run the application. Usage: make run
	uvicorn backend.app.main:app --reload --workers 1 --host 0.0.0.0 --port 8000

search: ## Searchs for a token in the code. Usage: make search token=your_token
	grep -rnw . --exclude-dir=venv --exclude-dir=.git --exclude=poetry.lock -e "$(token)"

sudo: ## 
	docker exec -it fileserver-web-1 python manage.py createsuperuser

replace: ## Replaces a token in the code. Usage: make replace token=your_token
	sed -i 's/$(token)/$(new_token)/g' $$(grep -rl "$(token)" . \
		--exclude-dir=venv \
		--exclude-dir=.git \
		--exclude=poetry.lock)

minimal-requirements: ## Generates minimal requirements. Usage: make requirements
	python3 scripts/clean_packages.py requirements.txt requirements.txt

lint: ## perform inplace lint fixes
	@ruff check --unsafe-fixes --fix .
	@black $(shell git ls-files '*.py')

pylint:
	@pylint backend/

report: test ## Generate coverage report. Usage: make report
	coverage report --omit=$(OMIT_PATHS) --show-missing

ps: ## List all containers. Usage: make ps
	docker ps -a

build: ## Build the application. Usage: make build
	docker-compose build --no-cache

down: ## Down the application. Usage: make down
	docker-compose down

up: ## Up the application. Usage: make up
	docker-compose up --build --remove-orphans -d

restart: down up ## Restart the application. Usage: make restart

pid: ## Show container pid. Usage: make pid
	docker inspect --format '{{.State.Pid}}' ${container}

ip: ## Show container ip. Usage: make ip
	docker inspect --format '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' ${container}

kill: ## Kill a container. Usage: make kill container_name=your_container_name
	docker inspect --format '{{.State.Pid}}' ${container} | xargs -I {} sudo kill {}

kill-all: ## Kill all containers with names starting with the specified token. Usage: make kill token=your_token
	@token=${token:-fileserver}; \
	containers=$$(docker ps -q --filter "name=$$token"); \
	if [ -z "$$containers" ]; then \
	    echo "No containers found with name starting with $$token"; \
	    exit 0; \
	fi; \
	echo "Killing containers: $$containers"; \
	docker inspect --format '{{.State.Pid}}' $$containers | xargs -I {} sudo kill {}

psql: ## Access the database. Usage: make psql
	docker exec -it fileserver-db-1 psql -h localhost -U ${DATABASE_USER} ${DATABASE_NAME}

bash: ## Access the container. Usage: make bash container=your_container_name
	docker exec -it ${container} bash