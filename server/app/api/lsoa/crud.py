from sqlalchemy.sql import func
from app import db
from app.api.lsoa.models import LsoaCcgStpLookup
from app.logger import logger


def read_lsoa_lookup():
    return LsoaCcgStpLookup.query.all()


def read_lsoa_first_500():
    return LsoaCcgStpLookup.query.limit(100).all()
