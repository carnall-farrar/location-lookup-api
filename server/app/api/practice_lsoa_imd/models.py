from app import db


class PracticeToImd(db.Model):

    __tablename__ = "practice_lsoa_imd"

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(150), nullable=False)
    postcode = db.Column(db.String(50), nullable=False)
    postcode_status = db.Column(db.String(50), nullable=False)
    lsoa_code = db.Column(db.String(150), nullable=False)
    lsoa_name = db.Column(db.String(150), nullable=False)
    imd_rank = db.Column(db.Integer, nullable=False)
    imd_decile = db.Column(db.Integer, nullable=False)
    imcome_rank = db.Column(db.Integer, nullable=False)
    income_decile = db.Column(db.Integer, nullable=False)
    income_score = db.Column(db.Float, nullable=False)
    emplyment_rank = db.Column(db.Integer, nullable=False)
    employment_decile = db.Column(db.Integer, nullable=False)
    employment_score = db.Column(db.Float, nullable=False)
    education_skills_rank = db.Column(db.Integer, nullable=False)
    education_skills_decile = db.Column(db.Integer, nullable=False)
    health_disability_rank = db.Column(db.Integer, nullable=False)
    health_disability_decile = db.Column(db.Integer, nullable=False)
    crime_rank = db.Column(db.Integer, nullable=False)
    crime_decile = db.Column(db.Integer, nullable=False)
    barriers_to_housing_services_rank = db.Column(db.Integer, nullable=False)
    barriers_to_housing_services_decile = db.Column(db.Integer, nullable=False)
    living_environment_rank = db.Column(db.Integer, nullable=False)
    living_environment_decile = db.Column(db.Integer, nullable=False)
    IDACI_rank = db.Column(db.Integer, nullable=False)
    IDACI_decile = db.Column(db.Integer, nullable=False)
    IDACI_score = db.Column(db.Float, nullable=False)
    IDAOPI_rank = db.Column(db.Integer, nullable=False)
    IDAOPI_decile = db.Column(db.Integer, nullable=False)
    IDAOPI_score = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=db.func.current_timestamp())

    def __repr__(self):
        return f'<PracticeToImd {self.id}>'

    @classmethod
    def create(
        self,
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
        lookup_row = self(
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

        db.session.add(lookup_row)
        db.session.commit()
        return lookup_row
