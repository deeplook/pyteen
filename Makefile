.PHONY: all build install typing lint test

all: black build install typing lint test

black:
	black -l 79 --exclude "pyteen/snippets" pyteen tests
	black -l 79 $(find pyteen/snippets -name "test_*.py")
	# isort -rc --atomic pyteen tests

build:
	python3 -m pip install -r requirements.txt

clean: clean-build clean-pyc clean-test clean-doc ## remove all build, test, coverage and Python artifacts

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
	rm -f .coverage coverage.json coverage.xml
	rm -fr htmlcov/
	rm -fr .mypy_cache
	rm -fr .pytest_cache
	find . -name '.ipynb_checkpoints' -exec rm -fr {} +

clean-doc:
	pushd docs/guide && make clean && popd
	rm -f docs/adr/adr.html

doc:
	pushd docs/guide && make html && popd
	pushd docs/adr && adr-viewer --adr-path . --output adr.html && popd

install:
	python3 -m pip install -e .

typing:
	mypy --ignore-missing-imports pyteen tests

lint:
	isort --check -rc --diff pyteen tests
	# flake8 -v --statistics --count .
	black -l 79 --diff --check pyteen tests

test:
	pytest -s -v --cov-report=xml --cov=pyteen tests pyteen/snippets

snippet_coverage:
	coverage run --source=pyteen/snippets $(shell which pytest) -v -s pyteen/snippets
	coverage report -m --omit="*/__init__.py,*/test*.py" $(shell find pyteen/snippets -name "*.py")
	coverage json --omit="*/__init__.py,*/test*.py" $(shell find pyteen/snippets -name "*.py")
	python3 scripts/test_snippet_coverage.py

draft_changelog:
	proclamation draft $(shell python -c "from pyteen import __version__; print(__version__)")

build_changelog:
	proclamation build -o -r $(shell python -c "from pyteen import __version__; print(__version__)")

tree:
	tree .
