.PHONY: clean_db load_fixtures reset_migrations_and_db

mock: clean_db load_fake_data

load_users:
	python manage.py loaddata website/fixtures/fake/1-touchbelgium-users.json

clean_db:
	python manage.py flush

load_fake_data:
	for file in website/fixtures/fake/*.json; do \
		echo "Loading " $$file ;\
		python manage.py loaddata $$file; \
	done

delete_migrations:
	for file in website/migrations/*.py; do \
		rm $$file; \
	done
	touch website/migrations/__init__.py

delete_sqlite_db:
	rm db.sqlite3

reset_migrations_and_db: delete_migrations delete_sqlite_db

migrations_and_migrate:
	python manage.py makemigrations
	python manage.py migrate
