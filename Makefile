run:
	@uvicorn workout_api.main:app --reload

docker:
	@docker-compose up -d

freeze:
	@pip freeze > requirements.txt

asyncpg:
	@pip install asyncpg

create-migrations:
	@PYTHONPATH=$PYTHONPATH:$(pwd) alembic revision --autogenerate -m $(d)

run-migrations:
	@PYTHONPATH=$PYTHONPATH:$(pwd) alembic upgrade head

settings:
	@pip install pydantic-settings

paginate:
	@pip install fastapi-pagination