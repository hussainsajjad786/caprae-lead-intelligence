"""Illustrative B2B prospecting policy; not Caprae's investment criteria or an ML model."""
TARGET_INDUSTRIES = {'Technology', 'SaaS', 'FinTech', 'Healthcare', 'AI', 'Cybersecurity'}
TARGET_MARKETS = {'United States', 'Canada', 'United Kingdom'}
MAX_POINTS = {'Company size': 25, 'Industry fit': 25, 'Revenue fit': 20, 'Market fit': 10, 'Format checks': 10, 'Completeness': 10}


def priority_for(score: int) -> str:
    return 'High' if score >= 75 else 'Medium' if score >= 50 else 'Low'


def score_lead(data: dict, quality: dict) -> dict:
    size, revenue = data.get('employees') or 0, data.get('revenue') or 0
    values = [
        ('Company size', 25 if size >= 200 else 20 if size >= 50 else 12 if size >= 10 else 5 if size > 0 else 0, '200+: 25; 50–199: 20; 10–49: 12; 1–9: 5; missing/zero: 0'),
        ('Industry fit', 25 if data.get('industry') in TARGET_INDUSTRIES else 5 if data.get('industry') else 0, 'Target sector: 25; other sector: 5; missing: 0'),
        ('Revenue fit', 20 if revenue >= 10_000_000 else 15 if revenue >= 5_000_000 else 10 if revenue >= 1_000_000 else 5 if revenue > 0 else 0, 'USD 10M+: 20; 5M+: 15; 1M+: 10; positive: 5; missing/zero: 0'),
        ('Market fit', 10 if data.get('location') in TARGET_MARKETS else 3 if data.get('location') else 0, 'US, Canada, UK: 10; other market: 3; missing: 0'),
        ('Format checks', 5 * (quality['email_valid'] + quality['website_valid']), 'Email syntax: 5; website syntax: 5. No external verification.'),
        ('Completeness', round(quality['data_completeness'] / 10), '10 points × fraction of 8 populated core fields'),
    ]
    reasons = [dict(label=label, points=points, maximum=MAX_POINTS[label], explanation=explanation) for label, points, explanation in values]
    total = sum(x['points'] for x in reasons)
    return dict(lead_score=total, priority=priority_for(total), score_reasons=reasons)
