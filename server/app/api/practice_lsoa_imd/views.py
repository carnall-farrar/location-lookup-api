from flask import request, send_file
from flask_restx import Resource, fields, Namespace
from app.api.practice_lsoa_imd.crud import read_practice_imd_first_100

practiceImd_namespace = Namespace("practiceImd")

practiceImdModel = practiceImd_namespace.model(
    "practiceImd",
    {
        "id": fields.Integer(readOnly=True),
        "code": fields.String(required=True),
        "name": fields.String(required=True),
        "address": fields.String(required=True),
        "postcode": fields.String(required=True),
        "postcode_status": fields.String(required=True),
        "lsoa_code": fields.String(required=True),
        "lsoa_name": fields.String(required=True),
        "imd_rank": fields.Integer(required=True),
        "imd_decile": fields.Integer(required=True),
        "imcome_rank": fields.Integer(required=True),
        "income_decile": fields.Integer(required=True),
        "income_score": fields.Float(required=True),
        "emplyment_rank": fields.Integer(required=True),
        "employment_decile": fields.Integer(required=True),
        "employment_score": fields.Float(required=True),
        "education_skills_rank": fields.Integer(required=True),
        "education_skills_decile": fields.Integer(required=True),
        "health_disability_rank": fields.Integer(required=True),
        "health_disability_decile": fields.Integer(required=True),
        "crime_rank": fields.Integer(required=True),
        "crime_decile": fields.Integer(required=True),
        "barriers_to_housing_services_rank": fields.Integer(required=True),
        "barriers_to_housing_services_decile": fields.Integer(required=True),
        "living_environment_rank": fields.Integer(required=True),
        "living_environment_decile": fields.Integer(required=True),
        "IDACI_rank": fields.Integer(required=True),
        "IDACI_decile": fields.Integer(required=True),
        "IDACI_score": fields.Float(required=True),
        "IDAOPI_rank": fields.Integer(required=True),
        "IDAOPI_decile": fields.Integer(required=True),
        "IDAOPI_score": fields.Float(required=True),
        "created_at": fields.DateTime,
    },
)


class PracticeImdFirst100(Resource):
    @practiceImd_namespace.marshal_with(practiceImdModel, as_list=True)
    @practiceImd_namespace.response(200, "Success")
    @practiceImd_namespace.response(404, "No Locations Found")
    def get(self):
        """Returns first 100 rows of practice -> lsoa -> IMD lookup table"""
        return read_practice_imd_first_100(), 200


practiceImd_namespace.add_resource(PracticeImdFirst100, "")
