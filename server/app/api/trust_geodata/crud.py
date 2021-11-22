from app import db
from app.logger import logger
from app.api.trust_geodata.models import AllTrustGeodata


def createTrustGeodataRow(
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
):
    trustGeoRow = AllTrustGeodata.create(
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
        Longitude=Longitude
    )
    return trustGeoRow


def read_trust_geo_first_500():
    return AllTrustGeodata.query.limit(100).all()
