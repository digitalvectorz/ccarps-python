# Nicked this from Hy
# https://github.com/hylang/hy/blob/master/Makefile


all:
	@echo "No default step. Use setup.py"
	@echo ""
	@echo " Other targets:"
	@echo ""
	@echo "   - docs"
	@echo "   - full"
	@echo ""
	@echo "   - dev (test & flake)"
	@echo "   - flake"
	@echo "   - test"
	@echo "   - diff"
	@echo "   - d"
	@echo "   - r"
	@echo "   - clean"
	@echo ""

docs:
	make -C docs html

upload: r
	python setup.py sdist upload

full: d docs

venv:
ifeq (,$(findstring ccarps,$(VIRTUAL_ENV)))
	@echo "You're not in a ccarps virtualenv. Exiting."
	exit 1
else
	@echo "We're properly in a virtualenv. Going ahead."
endif

dev: test flake

test: venv
	nosetests -sv

flake:
	flake8 ccarps tests

clear:
	clear

d: clear dev

diff:
	git diff --color | less -r

r: d diff

travis:
	nosetests --with-coverage --cover-package ccarps
ifeq (PyPy,$(findstring PyPy,$(shell python -V 2>&1 | tail -1)))
	@echo "skipping flake8 on pypy"
else
	flake8 ccarps tests
endif

clean:
	@find . -name "*.pyc" -exec rm {} \;
	@find -name __pycache__ -delete
	@${RM} -r -f dist
	@${RM} -r -f *.egg-info
	@${RM} -r -f docs/_build

.PHONY: docs

