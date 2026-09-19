from sqlalchemy import select, func
from app.models import Lead, DuplicateReview
from app.seed.demo_data import demo_records, seed
from app.services.deduplication import ingest_lead


def test_duplicate_domain_is_preserved_for_review(db):
    row = demo_records()[0]
    original, created = ingest_lead(db, row)
    assert created
    incoming = {**row, 'website': 'http://www.aster-cloud.example.com/', 'company_name': 'Another name'}
    match, created = ingest_lead(db, incoming)
    assert not created and match.id == original.id
    assert db.scalar(select(func.count()).select_from(Lead)) == 1
    audit = db.scalar(select(DuplicateReview))
    assert audit.original_record == incoming


def test_name_fallback_and_different_domain_companies(db):
    row = {**demo_records()[0], 'website': None}
    original, _ = ingest_lead(db, row)
    _, created = ingest_lead(db, {**row, 'company_name': ' ASTER CLOUD (DEMO) '})
    assert not created
    _, created = ingest_lead(db, {**row, 'location': 'Germany'})
    assert created


def test_distinct_domains_are_not_merged_on_name_alone(db):
    row = demo_records()[0]
    ingest_lead(db, row)
    _, created = ingest_lead(db, {**row, 'website': 'https://different.example.com'})
    assert created


def test_seed_is_idempotent(db):
    seed(db)
    seed(db)
    assert db.scalar(select(func.count()).select_from(Lead)) == 32
    assert db.scalar(select(func.count()).select_from(DuplicateReview)) == 2
