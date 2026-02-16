install:
	python -m venv venv
	. venv/bin/activate && pip install -r requirements.txt


run:
	uvicorn app.main:app --reload


db-init:
	psql -h localhost -p 5433 -U postgres -d vector db -f init.sql


format:
	black app
