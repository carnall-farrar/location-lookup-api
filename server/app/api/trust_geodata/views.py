from flask import request, send_file
from flask_restx import Resource, fields, Namespace
from app.api.trust_geodata.crud import read_trust_geo_first_500

trustGeo_namespace = Namespace("trustGeodata")

trustGeo = trustGeo_namespace.model(
    "TrustGeo",
    {
        "id": fields.Integer(readOnly=True),
        "OrganisationCode": fields.String(required=True),
        "OrganisationType": fields.String(required=True),
        "SubType": fields.String(required=True),
        "Sector": fields.String(required=True),
        "OrganisationStatus": fields.String(required=True),
        "OrganisationName": fields.String(required=True),
        "Address1": fields.String(required=True),
        "Address2": fields.String(required=True),
        "Address3": fields.String(required=True),
        "City": fields.String(required=True),
        "County": fields.String(required=True),
        "Postcode": fields.String(required=True),
        "y": fields.String(required=True),
        "x": fields.String(required=True),
        "ParentODSCode": fields.String(required=True),
        "ParentName": fields.String(required=True),
        "Organisation": fields.String(required=True),
        "min_travel_time_destination": fields.String(required=True),
        "Latitude": fields.String(required=True),
        "Longitude": fields.String(required=True),
        "created_at": fields.DateTime,
    },
)


class TrustGeoFirst500(Resource):
    @trustGeo_namespace.marshal_with(trustGeo, as_list=True)
    @trustGeo_namespace.response(200, "Success")
    @trustGeo_namespace.response(404, "No Locations Found")
    def get(self):
        """Returns first 100 rows of trust geodata"""
        return read_trust_geo_first_500(), 200


trustGeo_namespace.add_resource(TrustGeoFirst500, "")
