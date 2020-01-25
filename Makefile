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

dump_db:
	python manage.py dumpdata auth.User > 1-touchbelgium-users.json --indent 2
	python manage.py dumpdata website.Venue > 1-touchbelgium-venues.json --indent 2
	python manage.py dumpdata website.Tag > 1-touchbelgium-tags.json --indent 2
	python manage.py dumpdata website.Contact > 1-touchbelgium-contacts.json --indent 2
	python manage.py dumpdata website.BannerPicture > 2-touchbelgium-banner-pictures.json --indent 2
	python manage.py dumpdata website.Team > 2-touchbelgium-teams.json --indent 2
	python manage.py dumpdata website.Link > 2-touchbelgium-links.json --indent 2
	python manage.py dumpdata website.File > 2-touchbelgium-files.json --indent 2
	python manage.py dumpdata website.Competition > 2-touchbelgium-competitions.json --indent 2
	python manage.py dumpdata website.Gallery > 3-touchbelgium-galleries.json --indent 2
	python manage.py dumpdata website.TBMember > 3-touchbelgium-tbmembers.json --indent 2
	python manage.py dumpdata website.Category > 3-touchbelgium-categories.json --indent 2
	python manage.py dumpdata website.Picture > 4-touchbelgium-pictures.json --indent 2
	python manage.py dumpdata website.Pool > 4-touchbelgium-pools.json --indent 2
	python manage.py dumpdata website.Match > 5-touchbelgium-matches.json --indent 2
