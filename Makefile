PYTHON := python3

.PHONY: install run debug clean lint

install:
	$(PYTHON) -m pip install -e .

run:
	$(PYTHON) a_maze_ing.py config.txt

debug:
	PYTHONFAULTHANDLER=1 $(PYTHON) a_maze_ing.py config.txt

clean:
	find . -type d -name "__pycache__" -prune -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -prune -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -prune -exec rm -rf {} +
	find . -type d -name "*.egg-info" -prune -exec rm -rf {} +
	rm -rf build dist

lint:
	flake8 .
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
