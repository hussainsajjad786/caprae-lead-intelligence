from sqlalchemy import select
from ..models import Lead
from ..services.deduplication import ingest_lead

NAMES = ['Aster Cloud', 'Northstar Analytics', 'Juniper Health', 'Cobalt Shield', 'Lumen Finance', 'Cedar AI', 'Orbit Systems', 'Willow Retail', 'Harbor Logistics', 'Ember Studio', 'Atlas Software', 'Fern Medical', 'Quill Security', 'Mosaic Labs', 'Solstice Data', 'Birch Manufacturing', 'Opal Networks', 'Finch Commerce', 'Aurora Insights', 'Maple Digital', 'Tidal Works', 'Nova Clinics', 'Sage Automation', 'Prism Services', 'Echo Devices', 'Meadow Foods', 'Violet Systems', 'Canyon Payments', 'Kite Robotics', 'Coral Learning', 'Pine Ventures', 'Silverline Tech']
INDUSTRIES = ['SaaS', 'Technology', 'Healthcare', 'Cybersecurity', 'FinTech', 'AI', 'Technology', 'Retail']
MARKETS = ['United States', 'Canada', 'United Kingdom', 'Germany', 'Pakistan', 'United States', 'United Kingdom', 'Canada']


def demo_records():
    rows = []
    for i, name in enumerate(NAMES):
        slug = name.lower().replace(' ', '-')
        row = dict(company_name=name + ' (Demo)', website=f'https://{slug}.example.com',
                   email=f'sales@{slug}.example.com', phone=f'+1-202-555-{100+i:04d}',
                   industry=INDUSTRIES[i % 8], location=MARKETS[i % 8],
                   employees=[240, 85, 32, 420, 15, 7, 110, 4][i % 8],
                   revenue=[18_000_000, 7_000_000, 2_500_000, 32_000_000, 1_200_000, 450_000, 9_000_000, 180_000][i % 8])
        if i % 7 == 4:
            row.update(email='sales-at-invalid', phone=None)
        if i % 9 == 7:
            row.update(website='not a url', email=None, revenue=None, employees=None)
        if i % 11 == 9:
            row.update(industry=None, location=None, phone=None)
        rows.append(row)
    rows.append({**rows[0], 'company_name': 'Aster Cloud Alternate (Demo)', 'website': 'http://www.aster-cloud.example.com/'})
    rows.append({**rows[7], 'company_name': ' WILLOW   RETAIL (DEMO) '})
    return rows


def seed(db):
    if db.scalar(select(Lead.id).limit(1)) is None:
        for row in demo_records():
            ingest_lead(db, row)
        db.commit()
