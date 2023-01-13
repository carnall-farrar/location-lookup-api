import logging

from app import db


class LsoaCcgStpLookup(db.Model):

    __tablename__ = "lsoa_ccg_stp_lookup"

    id = db.Column(db.Integer, primary_key=True)
    lsoa_code = db.Column(db.String(50), nullable=False)
    lsoa_name = db.Column(db.String(50), nullable=False)
    ccg_code = db.Column(db.String(50), nullable=False)
    ccg_cdh = db.Column(db.String(50), nullable=False)
    ccg_name = db.Column(db.String(500), nullable=False)
    stp_code = db.Column(db.String(50), nullable=False)
    stp_name = db.Column(db.String(500), nullable=False)
    local_authority_code = db.Column(db.String(500), nullable=False)
    local_authority_name = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=db.func.current_timestamp())

    def __repr__(self):
        return f'<LsoaCcgStpLookup {self.id}>'

    @classmethod
    def create(
        self,
        lsoa_code,
        lsoa_name,
        ccg_code,
        ccg_cdh,
        ccg_name,
        stp_code,
        stp_name,
        local_authority_code,
        local_authority_name
    ):
        lsoa_row = self(
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
        try:
            db.session.add(lsoa_row)
            db.session.commit()
        except Exception as e:
            logging.info(e)
        return lsoa_row
