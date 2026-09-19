from datetime import datetime, timezone
from sqlalchemy import Boolean, DateTime, Float, Integer, JSON, String
from sqlalchemy.orm import Mapped, mapped_column
from .database import Base


class Lead(Base):
    __tablename__ = 'leads'
    id: Mapped[int] = mapped_column(primary_key=True)
    company_name: Mapped[str] = mapped_column(String(160))
    normalized_company_name: Mapped[str] = mapped_column(String(160), index=True)
    normalized_domain: Mapped[str | None] = mapped_column(String(253), unique=True, index=True)
    website: Mapped[str | None] = mapped_column(String(500))
    industry: Mapped[str | None] = mapped_column(String(80), index=True)
    location: Mapped[str | None] = mapped_column(String(80), index=True)
    employees: Mapped[int | None] = mapped_column(Integer)
    revenue: Mapped[float | None] = mapped_column(Float)
    email: Mapped[str | None] = mapped_column(String(254))
    phone: Mapped[str | None] = mapped_column(String(40))
    linkedin_url: Mapped[str | None] = mapped_column(String(500), default=None)
    lead_score: Mapped[int] = mapped_column(Integer, index=True)
    priority: Mapped[str] = mapped_column(String(12), index=True)
    verification_status: Mapped[str] = mapped_column(String(30))
    email_valid: Mapped[bool] = mapped_column(Boolean)
    website_valid: Mapped[bool] = mapped_column(Boolean)
    is_duplicate: Mapped[bool] = mapped_column(Boolean, default=False)
    data_completeness: Mapped[int] = mapped_column(Integer)
    quality_score: Mapped[int] = mapped_column(Integer)
    quality_label: Mapped[str] = mapped_column(String(30))
    score_reasons: Mapped[list] = mapped_column(JSON)
    quality_flags: Mapped[list] = mapped_column(JSON)
    source: Mapped[str] = mapped_column(String(50), default='Demo / Synthetic Data')
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))


class DuplicateReview(Base):
    __tablename__ = 'duplicate_reviews'
    id: Mapped[int] = mapped_column(primary_key=True)
    incoming_company: Mapped[str] = mapped_column(String(160))
    matched_lead_id: Mapped[int] = mapped_column(Integer)
    reason: Mapped[str] = mapped_column(String(160))
    original_record: Mapped[dict] = mapped_column(JSON)
