from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Lead, DuplicateReview
from ..schemas import Filters, LeadOut, LeadsPage, DuplicateOut

router = APIRouter(prefix='/api')


def filtered_query(filters: Filters):
    if filters.min_score > filters.max_score:
        raise HTTPException(422, 'Minimum score cannot exceed maximum score')
    query = select(Lead).where(Lead.lead_score.between(filters.min_score, filters.max_score))
    if filters.search.strip():
        query = query.where(Lead.company_name.icontains(filters.search.strip(), autoescape=True))
    for field in ('industry', 'location', 'priority', 'verification_status'):
        value = getattr(filters, field)
        if value:
            query = query.where(getattr(Lead, field) == value)
    return query


@router.get('/leads', response_model=LeadsPage)
def list_leads(filters: Filters = Depends(), offset: int = Query(0, ge=0), limit: int = Query(50, ge=1, le=100), db: Session = Depends(get_db)):
    query = filtered_query(filters)
    total = db.scalar(select(func.count()).select_from(query.subquery()))
    rows = db.scalars(query.order_by(Lead.lead_score.desc(), Lead.id).offset(offset).limit(limit)).all()
    return dict(items=rows, total=total, offset=offset, limit=limit)


@router.get('/industries', response_model=list[str])
def industries(db: Session = Depends(get_db)):
    return db.scalars(select(Lead.industry).where(Lead.industry.is_not(None)).distinct().order_by(Lead.industry)).all()


@router.get('/locations', response_model=list[str])
def locations(db: Session = Depends(get_db)):
    return db.scalars(select(Lead.location).where(Lead.location.is_not(None)).distinct().order_by(Lead.location)).all()


@router.get('/quality/duplicates', response_model=list[DuplicateOut])
def duplicates(db: Session = Depends(get_db)):
    return db.scalars(select(DuplicateReview).order_by(DuplicateReview.id)).all()


@router.get('/leads/{lead_id}', response_model=LeadOut)
def lead_detail(lead_id: int, db: Session = Depends(get_db)):
    lead = db.get(Lead, lead_id)
    if not lead:
        raise HTTPException(404, 'Lead not found')
    return lead
