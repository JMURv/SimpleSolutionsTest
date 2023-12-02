db:
	poetry run python manage.py makemigrations
	poetry run python manage.py migrate
start:
	poetry run python manage.py runserver localhost:8000
items:
	poetry run python manage.py create_items

prod:
	docker-compose up

dev:
	docker-compose -f docker-compose.dev.yml up

down:
	docker-compose down
