build:
	pipenv run python notebooks/make_data.py
	docker compose up -d --build
	docker compose exec app python manage.py recreate_db
	docker compose exec app python manage.py add_ccg_lookup
	docker compose exec app python manage.py add_words
	docker compose exec app python manage.py add_words_index

up:
	pipenv run python notebooks/make_data.py
	docker compose up -d
	docker compose exec app python manage.py recreate_db
	docker compose exec app python manage.py add_ccg_lookup
	docker compose exec app python manage.py add_words
	docker compose exec app python manage.py add_words_index

test:
	docker compose exec app python -m pytest "app/tests" -p no:warnings

coverage:
	docker compose exec app python -m pytest "app/tests" -p no:warnings --cov="project"

lint:
	docker compose exec app flake8 app

lint_black: lint
	docker compose exec app black project --check
	docker compose exec app /bin/sh -c "isort app/**/*.py --check-only"

black:
	docker compose exec app black app
	docker compose exec app /bin/sh -c "isort app/**/*.py"

clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete

down:
	docker compose down

docker_clean:
	docker rmi $(docker images -q)
	echo 'CLEAN'

test_client:
	docker compose exec client npm test

coverage_client:
	docker compose exec client react-scripts test --coverage

lint_client:
	docker compose exec client npm run lint

format_client:
	docker compose exec client npm run prettier:check
	docker compose exec client npm run prettier:write
