from app import db
from app.logger import logger
from app.api.practice_lsoa_imd.models import PracticeToImd


def createPracticeImdRow(
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
):
    practice_imd_row = PracticeToImd.create(
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
        IDAOPI_score=IDAOPI_score
    )
    return practice_imd_row


def read_practice_imd_first_100():
    return PracticeToImd.query.limit(100).all()
