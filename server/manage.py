import sys

from flask.cli import FlaskGroup

from app import create_app, db
from app.api.location.models import CcgToStpLookup, Words


# app = create_app()
cli = FlaskGroup(create_app=create_app)


@cli.command('recreate_db')
def recreate_db():
    db.drop_all()
    CcgToStpLookup.__table__.create(db.session.bind)
    Words.__table__.create(db.session.bind)
    # db.create_all()
    db.session.commit()


@cli.command('add_ccg_lookup')
def add_ccg_lookup():
    with open("data/combined_lookup.csv") as fp:
        lines = fp.readlines()

        for line in lines[1:]:
            split = line.split("|")
            row = CcgToStpLookup.create(
                ccg_code=split[1].strip(),
                ccg_name=split[2].strip(),
                stp_code=split[3].strip(),
                stp_cdh=split[8].strip(),
                stp_name=split[4].strip(),
                region_code=split[10].strip(),
                region_cdh=split[11].strip(),
                region_name=split[12].strip(),
                file=split[5].strip()
            )
            print(row)


@cli.command('add_words')
def add_words():
    add_words_snippet = db.DDL("""
        INSERT INTO words (word)
        SELECT word FROM ts_stat('
          SELECT to_tsvector(''simple'', ccg_code) ||
                 to_tsvector(''simple'', coalesce(ccg_name, '''')) ||
                 to_tsvector(''simple'', stp_code) ||
                 to_tsvector(''simple'', stp_cdh) ||
                 to_tsvector(''simple'', coalesce(stp_name, '''')) ||
                 to_tsvector(''simple'', region_code) ||
                 to_tsvector(''simple'', region_cdh) ||
                 to_tsvector(''simple'', coalesce(region_name, ''''))
            FROM ccg_lookup
        ');
    """)
    db.session.execute(add_words_snippet)
    db.session.commit()
    print("Words added")

if __name__ == '__main__':
    cli()
