from app import db


class AllTrustGeodata(db.Model):

    __tablename__ = "all_trust_geodata"
    id = db.Column(db.Integer, primary_key=True)
    OrganisationID = db.Column(db.String(50), nullable=False)
    OrganisationCode = db.Column(db.String(50), nullable=False)
    OrganisationType = db.Column(db.String(50), nullable=False)
    SubType = db.Column(db.String(50), nullable=False)
    Sector = db.Column(db.String(50), nullable=False)
    OrganisationStatus = db.Column(db.String(50), nullable=False)
    IsPimsManaged = db.Column(db.String(50), nullable=False)
    OrganisationName = db.Column(db.String(50), nullable=False)
    Address1 = db.Column(db.String(50), nullable=False)
    Address2 = db.Column(db.String(50), nullable=False)
    Address3 = db.Column(db.String(50), nullable=False)
    City = db.Column(db.String(50), nullable=False)
    County = db.Column(db.String(50), nullable=False)
    Postcode = db.Column(db.String(50), nullable=False)
    y = db.Column(db.String(50), nullable=False)
    x = db.Column(db.String(50), nullable=False)
    ParentODSCode = db.Column(db.String(50), nullable=False)
    ParentName = db.Column(db.String(50), nullable=False)
    Phone = db.Column(db.String(50), nullable=False)
    Email = db.Column(db.String(50), nullable=False)
    Website = db.Column(db.String(50), nullable=False)
    Fax = db.Column(db.String(50), nullable=False)
    Organisation = db.Column(db.String(50), nullable=False)
    min_travel_time_destination = db.Column(db.String(50), nullable=False)
    Latitude = db.Column(db.Float, nullable=False)
    Longitude = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=db.func.current_timestamp())

    def __repr__(self):
        return f'<AllTrustGeodata {self.id}>'

    @classmethod
    def create(
        self,
        OrganisationID,
        OrganisationCode,
        OrganisationType,
        SubType,
        Sector,
        OrganisationStatus,
        IsPimsManaged,
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
        Phone,
        Email,
        Website,
        Fax,
        Organisation,
        min_travel_time_destination,
        Latitude,
        Longitude
    ):
        trust_row = self(
            OrganisationID=OrganisationID,
            OrganisationCode=OrganisationCode,
            OrganisationType=OrganisationType,
            SubType=SubType,
            Sector=Sector,
            OrganisationStatus=OrganisationStatus,
            IsPimsManaged=IsPimsManaged,
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
            Phone=Phone,
            Email=Email,
            Website=Website,
            Fax=Fax,
            Organisation=Organisation,
            min_travel_time_destination=min_travel_time_destination,
            Latitude=Latitude,
            Longitude=Longitude
        )
        db.session.add(trust_row)
        db.session.commit()
        return trust_row
