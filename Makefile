PYTHON := python3

.PHONY: install package run debug clean lint

install:
	$(PYTHON) -m pip install -e .

package:
	@if $(PYTHON) -c "import setuptools" >/dev/null 2>&1; then \
		BUILD_PYTHON="$(PYTHON)"; \
	elif /usr/bin/python3 -c "import setuptools" >/dev/null 2>&1; then \
		BUILD_PYTHON="/usr/bin/python3"; \
	else \
		echo "Error: setuptools is required to build the package."; \
		exit 1; \
	fi; \
	$$BUILD_PYTHON -m pip wheel . --no-deps --no-build-isolation -w .

run:
	$(PYTHON) a_maze_ing.py config.txt

debug:
	$(PYTHON) -m pdb a_maze_ing.py config.txt

clean:
	find . -type d -name "__pycache__" -prune -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -prune -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -prune -exec rm -rf {} +
	find . -type d -name "*.egg-info" -prune -exec rm -rf {} +
	rm -rf build dist

lint:
	@if $(PYTHON) -c "import flake8, mypy" >/dev/null 2>&1; then \
		$(PYTHON) -m flake8 --jobs 1 .; \
		$(PYTHON) -m mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs; \
	else \
		echo "Error: flake8 and mypy must be installed in the active Python environment."; \
		echo "Install them with: $(PYTHON) -m pip install flake8 mypy"; \
		exit 1; \
	fi
