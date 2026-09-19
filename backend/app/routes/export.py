import csv
import io
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Lead
from ..schemas import Filters
from .leads import filtered_query

router = APIRouter()
FIELDS = ['company_name', 'industry', 'location', 'employees', 'revenue', 'email', 'website', 'phone', 'lead_score', 'priority', 'verification_status', 'quality_score', 'data_completeness', 'source']


def safe_cell(value):
    text = '' if value is None else str(value)
    # Neutralize spreadsheet formulas, including formulas preceded by whitespace.
    return "'" + text if text.lstrip().startswith(('=', '+', '-', '@')) or text.startswith(('\t', '\r', '\n')) else text


@router.get('/api/leads/export')
def export(filters: Filters = Depends(), db: Session = Depends(get_db)):
    rows = db.scalars(filtered_query(filters).order_by(Lead.lead_score.desc(), Lead.id)).all()
    output = io.StringIO(newline='')
    writer = csv.writer(output)
    writer.writerow(FIELDS)
    for row in rows:
        writer.writerow([safe_cell(getattr(row, field)) for field in FIELDS])
    return StreamingResponse(iter([output.getvalue()]), media_type='text/csv', headers={'Content-Disposition': 'attachment; filename="qualified-demo-leads.csv"', 'Cache-Control': 'no-store'})
