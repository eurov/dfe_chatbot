SHELL = /bin/bash
VENV_PATH = venv

venv: $(VENV_PATH)\state

$(VENV_PATH)\state: requirements.txt requirements_dev.txt
	echo "Start creating virtual environment"
	python -m venv $(VENV_PATH)
	$(VENV_PATH)\Scripts\pip install -r requirements.txt
	$(VENV_PATH)\Scripts\pip install -r requirements_dev.txt
	copy NUL $(VENV_PATH)\state

build:
	docker-compose build dfe_chatbot

up:
	docker-compose up -d

exec:
	docker exec -it dfe_chatbot python main.py

start_app: build up exec

format: venv
	$(VENV_PATH)\Scripts\black --line-length=120 .
.PHONY: format

run_db:
	docker-compose up -d ydb-local
	timeout 5

test: venv run_db
	$(VENV_PATH)\Scripts\python test_main.py
.PHONY: test

clean:
	rmdir $(VENV_PATH) /s /q
	docker-compose down