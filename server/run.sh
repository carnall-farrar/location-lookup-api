#!/bin/sh

python manage.py recreate_db

python manage.py add_ccg_lookup

python manage.py add_lsoa_lookup

python manage.py add_trust_geodata

python manage.py add_words

python manage.py add_words_index

python manage.py run -h 0.0.0.0