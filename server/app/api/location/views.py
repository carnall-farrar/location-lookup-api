from flask import request
from flask_restx import Resource, fields, Namespace

from app.logger import logger
from app.api.location.crud import (
    search_lookup,
    read_lookups,
    read_words,
    read_lookup_by_id,
    read_lookup_by_ccg_code,
    read_lookup_by_stp_code,
    read_lookup_by_region_code,
    create_lookup,
)


location_namespace = Namespace("location")

location = location_namespace.model(
    "Location",
    {
        "id": fields.Integer(readOnly=True),
        "ccg_code": fields.String(required=True),
        "ccg_name": fields.String(required=True),
        "stp_code": fields.String(required=True),
        "stp_cdh": fields.String(required=True),
        "stp_name": fields.String(required=True),
        "region_code": fields.String(required=True),
        "region_cdh": fields.String(required=True),
        "region_name": fields.String(required=True),
        "created_at": fields.DateTime,
    },
)

location_search = location_namespace.inherit(
    "LocationSearch",
    location,
    {
        "rank": fields.Float
    }
)

location_word = location_namespace.model(
    "LocationWord",
    {
        "word": fields.String(required=True)
    }
)


class Location(Resource):
    @location_namespace.marshal_with(location)
    @location_namespace.response(200, "Success")
    @location_namespace.response(404, "Location <location_id> does not exist")
    def get(self, location_id):
        """Returns a single location."""
        location = read_lookup_by_id(location_id)
        if not location:
            location_namespace.abort(404, f"Location {location_id} does not exist")
        return location, 200


class LocationList(Resource):
    @location_namespace.marshal_with(location, as_list=True)
    @location_namespace.response(200, "Success")
    @location_namespace.response(404, "No Locations Found")
    def get(self):
        """Returns all locations in DB"""
        return read_lookups(), 200


class LocationSearch(Resource):
    @location_namespace.marshal_with(location_search, as_list=True)
    @location_namespace.response(200, "Success")
    @location_namespace.response(404, "No Locations Match")
    def get(self):
        """Returns a list of locations to match search param."""
        search_query = request.args.get('query')
        search_query = search_query.replace(" ", "&")
        search_query = search_query.replace("+", "&")
        logger.debug(search_query)
        location_results = search_lookup(search_query)
        if not location_results:
            location_namespace.abort(404, f"No Locations Match")
        results = []
        for location_result in location_results:
            results.append({
                "id": location_result.id,
                "ccg_code": location_result.ccg_code,
                "ccg_name": location_result.ccg_name,
                "stp_code": location_result.stp_code,
                "stp_cdh": location_result.stp_cdh,
                "stp_name": location_result.stp_name,
                "region_code": location_result.region_code,
                "region_cdh": location_result.region_cdh,
                "region_name": location_result.region_name,
                "created_at": location_result.created_at,
                "rank": location_result.rank
            })
        return results, 200


class LocationSearchWords(Resource):
    @location_namespace.marshal_with(location_word, as_list=True)
    def get(self):
        search_query = request.args.get('query')
        logger.debug(f"Word Query: {search_query}")
        words = read_words(search_query)
        result = [{"word": word} for word in words]

        return result, 200


location_namespace.add_resource(LocationList, "")
location_namespace.add_resource(LocationSearchWords, "/words")
location_namespace.add_resource(LocationSearch, "/search")
location_namespace.add_resource(Location, "/<int:location_id>")
