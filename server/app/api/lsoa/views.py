from flask import request
from flask_restx import Resource, fields, Namespace

from app.logger import logger
from app.api.lsoa.crud import (
    read_lsoa_lookup
)


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


class Lsoa(Resource):
    @lsoa_namespace.marshal_with(lsoa, as_list=True)
    @lsoa_namespace.response(200, "Success")
    @lsoa_namespace.response(404, "No Locations Found")
    def get(self):
        """Returns all locations in DB"""
        return read_lsoa_lookup(), 200


lsoa_namespace.add_resource(Lsoa, "")
