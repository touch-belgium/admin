.PHONY: clean_db load_fixtures

all: clean_db load_fixtures

clean_db:
	python manage.py flush

load_fixtures:
	for file in website/fixtures/*.json; do \
		echo "Loading " $$file ;\
		python manage.py loaddata $$file; \
	done
