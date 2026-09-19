from fastapi import APIRouter, Depends
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Lead, DuplicateReview
from ..schemas import StatsOut

router = APIRouter()


@router.get('/api/stats', response_model=StatsOut)
def stats(db: Session = Depends(get_db)):
    total, average, quality = db.execute(select(func.count(Lead.id), func.avg(Lead.lead_score), func.avg(Lead.quality_score))).one()
    priorities = dict(db.execute(select(Lead.priority, func.count()).group_by(Lead.priority)).all())
    industries = {k or 'Unspecified': v for k, v in db.execute(select(Lead.industry, func.count()).group_by(Lead.industry))}
    valid = db.scalar(select(func.count()).select_from(Lead).where(Lead.verification_status == 'Format Valid'))
    return dict(total=total, high_priority=priorities.get('High', 0), format_valid=valid,
                average_score=round(average or 0, 1), average_quality=round(quality or 0, 1),
                needs_review=total-valid, duplicates_prevented=db.scalar(select(func.count()).select_from(DuplicateReview)),
                priorities=priorities, industries=industries)
