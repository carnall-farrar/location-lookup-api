from sqlalchemy.dialects.postgresql import TSVECTOR
import logging as logger

from app import db


class CcgToStpLookup(db.Model):

    __tablename__ = "ccg_lookup"

    __table_args__ = (db.Index('tsv_idx', 'tsv_searchable_text', postgresql_using='gin'),)

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
            ccg_code=ccg_code,
            ccg_name=ccg_name,
            stp_code=stp_code,
            stp_cdh=stp_cdh,
            stp_name=stp_name,
            region_code=region_code,
            region_cdh=region_cdh,
            region_name=region_name,
            file=file
        )

        db.session.add(lookup_row)
        db.session.commit()
        return lookup_row


class Words(db.Model):

    __tablename__ = "words"

    # __table_args__ = (db.Index('word_idx', 'word', postgresql_using = 'gin (word gin_trgm_ops)'),)

    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(200))

try:
    function_snippet = db.DDL("""
        CREATE FUNCTION tsv_searchable_text_trigger() RETURNS trigger AS $$
        begin
        new.tsv_searchable_text :=
            setweight(to_tsvector('pg_catalog.english', coalesce(new.ccg_code,'')), 'B') ||
            setweight(to_tsvector('pg_catalog.english', coalesce(new.ccg_name,'')), 'A') ||
            setweight(to_tsvector('pg_catalog.english', coalesce(new.stp_code,'')), 'C') ||
            setweight(to_tsvector('pg_catalog.english', coalesce(new.stp_cdh,'')), 'B') ||
            setweight(to_tsvector('pg_catalog.english', coalesce(new.stp_name,'')), 'A') ||
            setweight(to_tsvector('pg_catalog.english', coalesce(new.region_code,'')), 'C') ||
            setweight(to_tsvector('pg_catalog.english', coalesce(new.region_cdh,'')), 'B') ||
            setweight(to_tsvector('pg_catalog.english', coalesce(new.region_name,'')), 'A');
        return new;
        end
        $$ LANGUAGE plpgsql;
    """)
except Exception as e:
    logger.info(e)

try:
    trigger_snippet = db.DDL("""
        CREATE TRIGGER searchable_text_update BEFORE INSERT OR UPDATE
        ON ccg_lookup
        FOR EACH ROW EXECUTE PROCEDURE tsv_searchable_text_trigger();
    """)
except Exception as e:
    logger.info(e)

try:
    add_words_snippet = db.DDL("""
            INSERT INTO words (word)
            SELECT word FROM ts_stat('
            SELECT to_tsvector(''simple'', ccg_code) ||
                    to_tsvector(''simple'', coalesce(ccg_name, '''')) ||
                    to_tsvector(''simple'', stp_code) ||
                    to_tsvector(''simple'', stp_cdh) ||
                    to_tsvector(''simple'', coalesce(stp_name, '''')) ||
                    to_tsvector(''simple'', region_code) ||
                    to_tsvector(''simple'', region_cdh) ||
                    to_tsvector(''simple'', coalesce(region_name, ''''))
                FROM ccg_lookup
            ');
        """)
except Exception as e:
    logger.info(e)

db.event.listen(CcgToStpLookup.__table__, 'after_create', function_snippet.execute_if(dialect='postgresql'))
db.event.listen(CcgToStpLookup.__table__, 'after_create', trigger_snippet.execute_if(dialect='postgresql'))
# db.event.listen(CcgToStpLookup.__table__, 'after_insert', add_words_snippet.execute_if(dialect = 'postgresql'))
