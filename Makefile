.PHONY: all build install typing lint test

all: black build install typing lint test

black:
	black -l 79 pyteen tests
	isort -rc --atomic pyteen tests

build:
	python3 -m pip install -r requirements.txt

clean: clean-build clean-pyc clean-test ## remove all build, test, coverage and Python artifacts

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test: ## remove test and coverage artifacts
	# rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/
	rm -fr .mypy_cache
	rm -fr .pytest_cache
	find . -name '.ipynb_checkpoints' -exec rm -fr {} +

install:
	python3 -m pip install -e .

typing:
	pytest -v -s --mypy pyteen

lint:
	isort --check -rc --diff pyteen tests
	# flake8 -v --statistics --count .
	black -l 79 --diff --check pyteen tests

test:
	# pytest -v -s --cov=pyteen.py tests
	pytest -s -v tests pyteen/snippets/tests
	# coverage html

tree:
	tree .
