from app import db
from app.api.lsoa.models import LsoaCcgStpLookup


def createLsoaRow(
    lsoa_code, lsoa_name, ccg_code, ccg_cdh, ccg_name, stp_code, stp_name, local_authority_code, local_authority_name
):
    lsoaRow = LsoaCcgStpLookup.create(
        lsoa_code=lsoa_code,
        lsoa_name=lsoa_name,
        ccg_code=ccg_code,
        ccg_cdh=ccg_cdh,
        ccg_name=ccg_name,
        stp_code=stp_code,
        stp_name=stp_name,
        local_authority_code=local_authority_code,
        local_authority_name=local_authority_name
    )
    return lsoaRow
