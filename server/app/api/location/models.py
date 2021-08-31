from sqlalchemy.dialects.postgresql import TSVECTOR

from app import db


class CcgToStpLookup(db.Model):

    __tablename__ = "ccg_lookup"

    __table_args__ = (db.Index('tsv_idx', 'tsv_searchable_text', postgresql_using = 'gin'),)

    id = db.Column(db.Integer, primary_key=True)
    ccg_code = db.Column(db.String(50), nullable=False)
    ccg_name = db.Column(db.String(500), nullable=False)
    stp_code = db.Column(db.String(50), nullable=False)
    stp_cdh = db.Column(db.String(200), nullable=False)
    stp_name = db.Column(db.String(500), nullable=False)
    region_code = db.Column(db.String(200), nullable=False)
    region_cdh = db.Column(db.String(200), nullable=False)
    region_name = db.Column(db.String(200), nullable=False)
    file = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=db.func.current_timestamp())
    tsv_searchable_text = db.Column(TSVECTOR)

    def __repr__(self):
        return f'<CcgToStpLookup {self.id}>'

    @classmethod
    def create(
        self,
        ccg_code,
        ccg_name,
        stp_code,
        stp_cdh,
        stp_name,
        region_code,
        region_cdh,
        region_name,
        file
        ):
        lookup_row = self(
            ccg_code = ccg_code,
            ccg_name = ccg_name,
            stp_code = stp_code,
            stp_cdh =  stp_cdh,
            stp_name = stp_name,
            region_code = region_code,
            region_cdh = region_cdh,
            region_name = region_name,
            file = file
        )

        db.session.add(lookup_row)
        db.session.commit()
        return lookup_row

function_snippet = db.DDL("""
    CREATE FUNCTION tsv_searchable_text_trigger() RETURNS trigger AS $$
    begin
    new.tsv_searchable_text :=
        setweight(to_tsvector('pg_catalog.english', coalesce(new.ccg_code,'')), 'A') ||
        setweight(to_tsvector('pg_catalog.english', coalesce(new.ccg_name,'')), 'A') ||
        setweight(to_tsvector('pg_catalog.english', coalesce(new.stp_code,'')), 'B') ||
        setweight(to_tsvector('pg_catalog.english', coalesce(new.stp_cdh,'')), 'B') ||
        setweight(to_tsvector('pg_catalog.english', coalesce(new.stp_name,'')), 'B') ||
        setweight(to_tsvector('pg_catalog.english', coalesce(new.region_code,'')), 'C') ||
        setweight(to_tsvector('pg_catalog.english', coalesce(new.region_cdh,'')), 'C') ||
        setweight(to_tsvector('pg_catalog.english', coalesce(new.region_name,'')), 'C');
    return new;
    end
    $$ LANGUAGE plpgsql;
""")

trigger_snippet = db.DDL("""
    CREATE TRIGGER searchable_text_update BEFORE INSERT OR UPDATE
    ON ccg_lookup
    FOR EACH ROW EXECUTE PROCEDURE tsv_searchable_text_trigger();
""")

db.event.listen(CcgToStpLookup.__table__, 'after_create', function_snippet.execute_if(dialect = 'postgresql'))
db.event.listen(CcgToStpLookup.__table__, 'after_create', trigger_snippet.execute_if(dialect = 'postgresql'))
