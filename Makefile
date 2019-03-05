SPHINXPROJ    = sslproto37
TOXTARGETS    = py3{5,6,7}-linux

# Put it first so that "make" without argument is like "make help".
help:
	@echo "clean - let this project be near mint"
	@echo "test - run tests with coverage"
	@echo "black - run black formatter"
	@echo "fix-import - calls black and fix the imports"
	@echo "requirements-dev - installs development requirements"

.PHONY: help

black:
	black ./sslproto37 ./tests

fix-import: black
	isort -rc ./sslproto37

cleanpycache:
	find . -type d | grep "__pycache__" | xargs rm -rf

clean: cleanpycache
	rm -rf ./.coverage
	rm -rf ./.pytest_cache
	rm -rf ./.tox
	rm -rf ./build
	rm -rf ./dist
	rm -rf ./htmlcov
	rm -rf ./*.egg-info

requirements-dev:
	pip install pip-tools
	pip-compile -r -U requirements-dev.in -o requirements-dev.txt
	pip-sync requirements-dev.txt

test-local: clean
	tox -e `echo "$(TOXTARGETS)" | tr " " ","`

# release:
# 	tox -e check
# 	python setup.py clean --all sdist bdist
# 	twine upload --skip-existing dist/*.whl dist/*.gz dist/*.zip
