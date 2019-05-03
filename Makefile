.PHONY: all prepare-dev venv lint test run shell clean build test_upload upload
.PHONY: docker_influxdb docker_influxdb_shell docker_grafana docker_kill
PROJECT=clb

SHELL:=/bin/bash

VENV_NAME?=venv
PYTHON=$(shell pwd)/${VENV_NAME}/bin/python3


all:
	@echo "make prepare-dev"
	@echo "    Create python virtual environment and install dependencies."
	@echo "make lint"
	@echo "    Run lint on project."
	@echo "make test"
	@echo "    Run tests on project."
	@echo "make clean"
	@echo "    Remove python artifacts, docker/ and virtualenv"
	@echo "make build"
	@echo "    Creates Python package."
	@echo "make test_upload"
	@echo "    Uploads package to TEST PyPI."
	@echo "make upload"
	@echo "    Uploads package to PyPI."
	@echo "make docker_influxdb"
	@echo "    Run influxdb docker container."
	@echo "make docker_influxdb_shell"
	@echo "    Run influxdb shell docker container."
	@echo "make docker_grafana"
	@echo "    Run grafana docker container."
	@echo "make docker_kill"
	@echo "    Kill & rm project docker containers."

prepare-dev:
	which virtualenv || python3 -m pip install virtualenv
	make venv

venv: $(VENV_NAME)/bin/activate
$(VENV_NAME)/bin/activate: setup.py
	test -d $(VENV_NAME) || virtualenv -p python3 $(VENV_NAME)
	${PYTHON} -m pip install -U pip setuptools
	${PYTHON} -m pip install -e .[devel]
	touch $(VENV_NAME)/bin/activate

lint: venv
	${PYTHON} -m pylint --rcfile=.pylintrc ${PROJECT}
	${PYTHON} -m mypy --ignore-missing-imports ${PROJECT}

test: venv
	${PYTHON} -m pytest -vv tests

clean: docker_kill
	find . -name '*.pyc' -delete
	rm -rf $(VENV_NAME) *.eggs *.egg-info dist build docs/_build .cache
	rm -rf $(shell pwd)/docker

build: venv
	rm -rf dist/*
	${PYTHON} setup.py sdist bdist_wheel

test_upload: venv
	${PYTHON} -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*

upload: venv
	${PYTHON} -m twine upload dist/*

docker_influxdb: venv
	docker run -d -p 8086:8086 \
	-v $(shell pwd)/docker/influxdb:/var/lib/influxdb \
	--name=influxdb \
	influxdb || :

docker_influxdb_shell: venv docker_influxdb
	docker run --rm --net=container:influxdb \
	--name=influxdb_shell \
	-v $(shell pwd)/docker/influxdb:/root -w=/root -it \
	influxdb influx

docker_grafana: venv docker_influxdb
	docker run -d -p 3000:3000 \
	--name=grafana \
	-v $(shell pwd)/docker/influxdb:/var/lib/influxdb \
	grafana/grafana

docker_kill:
	docker rm -f grafana influxdb_shell influxdb || :
