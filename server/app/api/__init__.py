from flask_restx import Api

from app.api.ping import ping_namespace
from app.api.location.views import location_namespace
from app.api.lsoa.views import lsoa_namespace
from app.api.trust_geodata.views import trustGeo_namespace

api = Api(version="1.0", title="Backend API", doc="/doc/")

api.add_namespace(ping_namespace, path="/ping")
api.add_namespace(location_namespace, path="/location")
api.add_namespace(lsoa_namespace, path="/lsoa")
api.add_namespace(trustGeo_namespace, path="/trustGeo")
