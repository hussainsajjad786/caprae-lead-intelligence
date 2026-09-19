from sqlalchemy import select
from ..models import Lead, DuplicateReview
from .validation import normalize_domain, normalize_company_name
from .lead_quality import assess_quality
from .scoring import score_lead


def find_duplicate(db, data):
    domain = normalize_domain(data.get('website'))
    name = normalize_company_name(data['company_name'])
    if domain:
        match = db.scalar(select(Lead).where(Lead.normalized_domain == domain))
        if match:
            return match, 'Same normalized domain'
    # Name fallback is only safe enough to flag when either record lacks a domain.
    candidates = db.scalars(select(Lead).where(Lead.normalized_company_name == name, Lead.location == data.get('location')))
    for match in candidates:
        if not domain or not match.normalized_domain:
            return match, 'Same normalized company and market; domain unavailable'
    return None, None


def ingest_lead(db, data):
    match, reason = find_duplicate(db, data)
    if match:
        db.add(DuplicateReview(incoming_company=data['company_name'], matched_lead_id=match.id, reason=reason, original_record=data))
        db.flush()
        return match, False
    quality = assess_quality(data)
    lead = Lead(**data, normalized_domain=normalize_domain(data.get('website')),
                normalized_company_name=normalize_company_name(data['company_name']),
                **quality, **score_lead(data, quality))
    db.add(lead)
    db.flush()
    return lead, True
