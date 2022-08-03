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
	docker-compose build

run:
	docker-compose up -d

attach:
	docker attach dfe_chatbot

start_app: build run attach

format: venv
	$(VENV_PATH)\Scripts\black --line-length=120 .
.PHONY: format

run_postgres:
	docker-compose up -d postgres
	timeout 5

test: venv run_postgres
	$(VENV_PATH)\Scripts\python test_main.py
.PHONY: test

clean:
	rmdir $(VENV_PATH) /s /q
	docker-compose down