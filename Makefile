SHELL = /bin/bash

VENV_PATH = venv

venv:
	echo "Start creating virtual environment"
	python3 -m venv $(VENV_PATH)
	$(VENV_PATH)/bin/pip install -r requirements.txt
	$(VENV_PATH)/bin/pip install -r requirements_dev.txt
	docker-compose run postgres -d

format: venv
	$(VENV_PATH)/bin/black --line-length=120 .
.PHONY: format

test: venv
	python3 test_main.py
.PHONY: test

test_all: venv test format
.PHONY: test_all