.PHONY: install run test coverage format format-lic pre-commit

install:
	pip install -r requirements.txt

run:
	python src/main.py

test:
	python -m pytest

coverage:
	python -m pytest --cov=src --cov-report=term

format:
	python -m black src/ tests/

format-lic:
	python scripts/format_with_licenses.py

pre-commit:
	python -m black src/ tests/
	python scripts/format_with_licenses.py

menu:
	python scripts/menu.py
