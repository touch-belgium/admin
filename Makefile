.PHONY: clean_db load_fixtures

mock: clean_db load_fake_data

clean_db:
	python manage.py flush

load_fake_data:
	for file in website/fixtures/fake/*.json; do \
		echo "Loading " $$file ;\
		python manage.py loaddata $$file; \
	done
