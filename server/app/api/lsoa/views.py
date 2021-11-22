from flask import request, send_from_directory, abort
from flask_restx import Resource, fields, Namespace

from app.logger import logger
from app.api.lsoa.crud import (
    read_lsoa_lookup,
    read_lsoa_first_500
)

LSOA_DATA_PATH = 'static_data/all_hospital_locations.csv'


lsoa_namespace = Namespace("lsoa")

lsoa = lsoa_namespace.model(
    "LSOA",
    {
        "id": fields.Integer(readOnly=True),
        "lsoa_code": fields.String(required=True),
        "lsoa_name": fields.String(required=True),
        "ccg_code": fields.String(required=True),
        "ccg_cdh": fields.String(required=True),
        "ccg_name": fields.String(required=True),
        "stp_code": fields.String(required=True),
        "stp_name": fields.String(required=True),
        "local_authority_code": fields.String(required=True),
        "local_authority_name": fields.String(required=True),
        "created_at": fields.DateTime,
    },
)


class LsoaFirst500(Resource):
    @lsoa_namespace.marshal_with(lsoa, as_list=True)
    @lsoa_namespace.response(200, "Success")
    @lsoa_namespace.response(404, "No Locations Found")
    def get(self):
        """Returns first 500 rows of lsoa dataset"""
        return read_lsoa_first_500(), 200


class LsoaALL(Resource):
    @lsoa_namespace.response(200, "Success")
    def get(self):
        """Returns full LSOA dataset - for download to csv"""
        try:
            return send_from_directory(LSOA_DATA_PATH, filename='all_hospital_locations.csv',  as_attachment=True)
        except FileNotFoundError:
            abort(404)


lsoa_namespace.add_resource(LsoaFirst500, "")
lsoa_namespace.add_resource(LsoaALL, "/download")
