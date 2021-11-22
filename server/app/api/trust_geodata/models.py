from app import db


class AllTrustGeodata(db.Model):

    __tablename__ = "all_trust_geodata"

    id = db.Column(db.Integer, primary_key=True)
    OrganisationCode = db.Column(db.String(150), nullable=False)
    OrganisationType = db.Column(db.String(150), nullable=False)
    SubType = db.Column(db.String(150), nullable=False)
    Sector = db.Column(db.String(150), nullable=False)
    OrganisationStatus = db.Column(db.String(150), nullable=False)
    OrganisationName = db.Column(db.String(150), nullable=False)
    Address1 = db.Column(db.String(150), nullable=False)
    Address2 = db.Column(db.String(150), nullable=False)
    Address3 = db.Column(db.String(50), nullable=False)
    City = db.Column(db.String(150), nullable=False)
    County = db.Column(db.String(150), nullable=False)
    Postcode = db.Column(db.String(50), nullable=False)
    y = db.Column(db.Float, nullable=False)
    x = db.Column(db.Float, nullable=False)
    ParentODSCode = db.Column(db.String(50), nullable=False)
    ParentName = db.Column(db.String(150), nullable=False)
    Organisation = db.Column(db.String(250), nullable=False)
    min_travel_time_destination = db.Column(db.String(250), nullable=False)
    Latitude = db.Column(db.Float, nullable=False)
    Longitude = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=db.func.current_timestamp())

    def __repr__(self):
        return f'<AllTrustGeodata {self.id}>'

    @classmethod
    def create(
        self,
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
        Longitude
    ):
        trust_row = self(
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
        db.session.add(trust_row)
        db.session.commit()
        return trust_row
