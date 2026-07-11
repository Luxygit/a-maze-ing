
SRC			= a_maze_ing.py
CONFIG		= config.txt
VENV        = .venv
PYTHON      = $(VENV)/bin/python3
PIP         = $(VENV)/bin/pip3

all: install run

$(VENV):
	python3 -m venv $(VENV)

install: $(VENV)
	@if [ -f *.whl ]; then \
		$(PIP) install *.whl; \
	fi

run:
	$(PYTHON) $(SRC) $(CONFIG)

debug:
	$(PYTHON) -m pdb $(SRC) $(CONFIG)

clean:
	rm -rf __pycache__ */__pycache__ .mypy_cache

lint:
	flake8 .
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	flake8 .
	mypy . --strict

.PHONY: all install run debug clean lint lint-strict
