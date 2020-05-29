# This needs to be migrated away from pipenv

all:
	@echo "\t\`make test\` to run tests"
	@echo "\t\`make dev\` to install development version"
	@echo "\t\`make lint\` to run static typing tests"

dev :
	@pipenv install --dev
	@pipenv run pip install -e .
	@echo "installed development version; run \`pipenv shell\` to enter activated environment."

test:
	@pipenv run pytest --cov-report term-missing --cov=omms_telegram_collection tests/


lint :
	@echo "======== PYLINT ======="
	@pipenv run pylint --rcfile=.pylintrc omms_telegram_collection -f parseable -r n
	@echo "======== MYPY ======="
	@pipenv run mypy --ignore-missing-imports --follow-imports=skip omms_telegram_collection
	@echo "======== PYCODESTYLE ======="
	@pipenv run pycodestyle omms_telegram_collection --max-line-length=120
	@echo "======== PYDOCSTYLE  ======="
	@pipenv run pydocstyle omms_telegram_collection

remove:
	@echo "removing virtual environment..."
	@pipenv --rm

