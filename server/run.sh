#!/bin/sh

poetry run python manage.py recreate_db

poetry run python manage.py add_ccg_lookup

poetry run python manage.py add_lsoa_lookup

poetry run python manage.py add_trust_geodata

poetry run python manage.py add_words

poetry run python manage.py add_words_index

poetry run python manage.py run -h 0.0.0.0