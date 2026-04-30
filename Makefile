.PHONY: install run test coverage format format-lic pre-commit

install:
	pip install -r requirements.txt

run:
	python src/scaffold

test:
	python -m pytest tests/ --no-cov

coverage:
	python -m pytest tests/ --cov src --cov-report term --cov-report html
	python -c "import os; os.path.exists('.coverage') and os.remove('.coverage')"

format:
	python -m black src/ tests/

format-lic:
	python scripts/format_with_licenses.py

pre-commit:
	python -m black src/ tests/
	python scripts/format_with_licenses.py
	python -m pytest tests/

menu:
	python scripts/menu.py
