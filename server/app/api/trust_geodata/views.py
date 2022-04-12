from flask import request, send_file
from flask_restx import Resource, fields, Namespace
from app.api.trust_geodata.crud import read_org_by_parent, read_org_by_orgcode

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

trustQuery = trustGeo_namespace.model(
    "TrustQuery",
    {
        "codes": fields.List(fields.String)
    }
)


class TrustGeoProviderParent(Resource):
    @trustGeo_namespace.marshal_with(trustGeo, as_list=True)
    @trustGeo_namespace.response(200, "Success")
    @trustGeo_namespace.response(404, "No Locations Found")
    def get(self, parent_ods_code):
        """Returns trust geodata by parent ODS"""
        return read_org_by_parent(parent_ods_code), 200


class TrustGeoProvider(Resource):
    @trustGeo_namespace.marshal_with(trustGeo)
    @trustGeo_namespace.response(200, "Success")
    @trustGeo_namespace.response(404, "No Locations Found")
    def get(self, org_code):
        """Returns provider by org_code"""
        return read_org_by_orgcode(org_code)


class TrustGeoList(Resource):
    @trustGeo_namespace.expect(trustQuery, validate=True)
    @trustGeo_namespace.marshal_with(trustGeo, as_list=True)
    @trustGeo_namespace.response(200, "Success")
    @trustGeo_namespace.response(404, "No Locations Found")
    def post(self):
        """Query with List of Codes"""
        post_data = request.get_json()
        codes = post_data["codes"]
        names = []
        for code in codes:
            name = read_org_by_orgcode(code)
            names.append(name)
        return names


trustGeo_namespace.add_resource(TrustGeoProviderParent, "/parent/<parent_ods_code>")
trustGeo_namespace.add_resource(TrustGeoProvider, "/org/<org_code>")
trustGeo_namespace.add_resource(TrustGeoList, "")
