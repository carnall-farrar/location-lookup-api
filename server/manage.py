import sys
import json

from flask.cli import FlaskGroup

from app import create_app, db
from app.logger import logger
from app.api.location.models import CcgToStpLookup, Words
from app.api.lsoa.models import LsoaCcgStpLookup
from app.api.trust_geodata.models import AllTrustGeodata
from app.api.practice_lsoa_imd.models import PracticeToImd
from app.api.lsoa.lsoa_utils import createLsoaRow
from app.api.trust_geodata.crud import createTrustGeodataRow
from app.api.practice_lsoa_imd.crud import createPracticeImdRow


# app = create_app()
cli = FlaskGroup(create_app=create_app)


@cli.command('recreate_db')
def recreate_db():
    db.drop_all()
    CcgToStpLookup.__table__.create(db.session.bind)
    Words.__table__.create(db.session.bind)
    LsoaCcgStpLookup.__table__.create(db.session.bind)
    AllTrustGeodata.__table__.create(db.session.bind)
    PracticeToImd.__table__.create(db.session.bind)
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
            logger.info(row)


@cli.command('add_lsoa_lookup')
def add_lsoa_lookup():
    logger.info('Adding lsoa lookup rows')
    with open("data/lsoa_ccg_stp.txt") as fp:
        lines = fp.readlines()
        lsoaRows = 0
        for line in lines[1:]:
            [
                lsoa_code,
                lsoa_name,
                ccg_code,
                ccg_cdh,
                ccg_name,
                stp_code,
                stp_name,
                local_authority_code,
                local_authority_name,
            ] = line.split("\t")

            row = createLsoaRow(
                lsoa_code=lsoa_code,
                lsoa_name=lsoa_name,
                ccg_code=ccg_code,
                ccg_cdh=ccg_cdh,
                ccg_name=ccg_name,
                stp_code=stp_code,
                stp_name=stp_name,
                local_authority_code=local_authority_code,
                local_authority_name=local_authority_name.strip("\n")
            )
            lsoaRows += 1
    logger.info(f'Added lsoa lookup: {lsoaRows} rows')


@cli.command('add_practice_lsoa_imd')
def add_lsoa_lookup():
    logger.info('Adding practice -> lsoa -> imd rows')
    with open("data/practice_to_lsoa_to_imd.txt") as fp:
        lines = fp.readlines()
        rows = 0
        for line in lines[1:]:
            [
                code,
                name,
                address,
                postcode,
                postcode_status,
                lsoa_code,
                lsoa_name,
                imd_rank,
                imd_decile,
                imcome_rank,
                income_decile,
                income_score,
                emplyment_rank,
                employment_decile,
                employment_score,
                education_skills_rank,
                education_skills_decile,
                health_disability_rank,
                health_disability_decile,
                crime_rank,
                crime_decile,
                barriers_to_housing_services_rank,
                barriers_to_housing_services_decile,
                living_environment_rank,
                living_environment_decile,
                IDACI_rank,
                IDACI_decile,
                IDACI_score,
                IDAOPI_rank,
                IDAOPI_decile,
                IDAOPI_score
            ] = line.split("\t")

            row = createPracticeImdRow(
                code=code,
                name=name,
                address=address,
                postcode=postcode,
                postcode_status=postcode_status,
                lsoa_code=lsoa_code,
                lsoa_name=lsoa_name,
                imd_rank=imd_rank,
                imd_decile=imd_decile,
                imcome_rank=imcome_rank,
                income_decile=income_decile,
                income_score=income_score,
                emplyment_rank=emplyment_rank,
                employment_decile=employment_decile,
                employment_score=employment_score,
                education_skills_rank=education_skills_rank,
                education_skills_decile=education_skills_decile,
                health_disability_rank=health_disability_rank,
                health_disability_decile=health_disability_decile,
                crime_rank=crime_rank,
                crime_decile=crime_decile,
                barriers_to_housing_services_rank=barriers_to_housing_services_rank,
                barriers_to_housing_services_decile=barriers_to_housing_services_decile,
                living_environment_rank=living_environment_rank,
                living_environment_decile=living_environment_decile,
                IDACI_rank=IDACI_rank,
                IDACI_decile=IDACI_decile,
                IDACI_score=IDACI_score,
                IDAOPI_rank=IDAOPI_rank,
                IDAOPI_decile=IDAOPI_decile,
                IDAOPI_score=IDAOPI_score.strip("\n")
            )
            rows += 1
    logger.info(f'Added practice lsoa imd lookup: {rows} rows')


@cli.command('add_trust_geodata')
def add_trust_geodata():
    logger.info('Adding trust geodata rows')
    with open("data/all_hospital_locations.txt") as fp:
        lines = fp.readlines()
        geoRows = 0
        for line in lines[1:]:
            [
                OrganisationCode,
                OrganisationType,
                SubType,
                Sector,
                OrganisationStatus,
                OrganisationName,
                Address1,
                Address2,
                Address3,
                City,
                County,
                Postcode,
                y,
                x,
                ParentODSCode,
                ParentName,
                Organisation,
                min_travel_time_destination,
                Latitude,
                Longitude,
            ] = line.split("\t")

            row = createTrustGeodataRow(
                OrganisationCode=OrganisationCode,
                OrganisationType=OrganisationType,
                SubType=SubType,
                Sector=Sector,
                OrganisationStatus=OrganisationStatus,
                OrganisationName=OrganisationName,
                Address1=Address1,
                Address2=Address2,
                Address3=Address3,
                City=City,
                County=County,
                Postcode=Postcode,
                y=y,
                x=x,
                ParentODSCode=ParentODSCode,
                ParentName=ParentName,
                Organisation=Organisation,
                min_travel_time_destination=min_travel_time_destination,
                Latitude=Latitude,
                Longitude=Longitude.strip("\n")
            )
            geoRows += 1
    logger.info(f'Added trust geodata: {geoRows} rows')


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
    logger.info("Words added")


@cli.command('add_words_index')
def add_words_index():
    add_words_index_snippet = db.DDL("""
        CREATE EXTENSION pg_trgm;
        CREATE INDEX IF NOT EXISTS location_search_word_trigram_index
                ON words
             USING gin (word gin_trgm_ops);
    """)
    db.session.execute(add_words_index_snippet)
    db.session.commit()
    logger.info("Words index added")


if __name__ == '__main__':
    cli()
