# all: test lint
COVERAGE_THRESHOLD ?= 90

install_requirements:
	pip install --no-cache -r requirements.txt

test:
	pip install --no-cache pytest mock pytest-mock coverage ;
	coverage run -m pytest ;
	coverage report --fail-under=${COVERAGE_THRESHOLD}


lint:
	pip install --no-cache pylint
	find . -type f -name "*.py" | xargs pylint
