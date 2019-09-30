load_users:
	python manage.py loaddata website/fixtures/1-touchbelgium-users.json

load_all:
	for file in website/fixtures/*.json; do \
		echo "Loading " $$file ;\
		python manage.py loaddata $$file; \
	done

clean_db:
	python manage.py flush

delete_sqlite_db:
	rm db.sqlite3

# Careful !
delete_migrations:
	for file in website/migrations/*.py; do \
		rm $$file; \
	done
	touch website/migrations/__init__.py

migrations_and_migrate:
	python manage.py makemigrations
	python manage.py migrate

migrate:
	python manage.py migrate

# Good to start from scratch
reset_db: delete_sqlite_db migrate load_all
