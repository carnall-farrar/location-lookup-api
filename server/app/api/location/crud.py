from sqlalchemy.sql import func
from app import db
from app.api.location.models import CcgToStpLookup, Words
from app.logger import logger


def create_lookup(
    ccg_code,
    ccg_name,
    stp_code,
    stp_cdh,
    stp_name,
    region_code,
    region_cdh,
    region_name
):
    lookup = CcgToStpLookup.create(
        ccg_code,
        ccg_name,
        stp_code,
        stp_cdh,
        stp_name,
        region_code,
        region_cdh,
        region_name
    )
    return lookup


def read_lookups():
    return CcgToStpLookup.query.all()


def read_lookup_by_id(lookup_id):
    return CcgToStpLookup.query.filter_by(id=lookup_id).first()


def read_lookup_by_ccg_code(ccg_code):
    return CcgToStpLookup.query.filter_by(ccg_code=ccg_code).first()


def read_lookup_by_stp_code(stp_code):
    return CcgToStpLookup.query.filter_by(stp_code=stp_code).first()


def read_lookup_by_region_code(region_code):
    return CcgToStpLookup.query.filter_by(region_code=region_code).first()


def search_lookup(search_query):

    results = db.session.query(
        CcgToStpLookup.id,
        CcgToStpLookup.ccg_code,
        CcgToStpLookup.ccg_name,
        CcgToStpLookup.stp_code,
        CcgToStpLookup.stp_cdh,
        CcgToStpLookup.stp_name,
        CcgToStpLookup.region_code,
        CcgToStpLookup.region_cdh,
        CcgToStpLookup.region_name,
        CcgToStpLookup.created_at,
        func.ts_rank_cd(CcgToStpLookup.tsv_searchable_text, func.plainto_tsquery(
            search_query, postgresql_regconfig='english'), 32).label('rank')
    ).filter(
        CcgToStpLookup.tsv_searchable_text.match(search_query, postgresql_regconfig='english')
    ).order_by(db.text('rank DESC')).limit(10)

    return results


def read_words(search_query):

    # words = db.session.query(
    #     Words.word,
    #     db.text(f'similarity({Words.word}, {search_query})').label('similarity')
    # ).filter(
    #     db.text(f'similarity({Words.word}, {search_query})') >= 0.3
    # ).order_by(db.text('similarity DESC')).limit(5)

    words_object = db.session.execute(
        db.text(f"""
            SELECT word, similarity(word, '{search_query}') AS similarity
            FROM words
            WHERE similarity(word, '{search_query}') >= 0.3
            ORDER BY similarity DESC;
        """)
    )

    words_result = []

    for r in words_object:
        logger.debug(f"result_object: {r}")
        word = r[0]
        words_result.append(word)

    logger.debug(words_result)

    return words_result


def update_lookup():
    pass


def delete_lookup():
    pass
