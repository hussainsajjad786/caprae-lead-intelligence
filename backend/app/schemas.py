from datetime import datetime
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field


class ScoreReason(BaseModel):
    label: str
    points: int
    maximum: int
    explanation: str


class LeadOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    company_name: str
    normalized_company_name: str
    normalized_domain: str | None
    website: str | None
    industry: str | None
    location: str | None
    employees: int | None
    revenue: float | None
    email: str | None
    phone: str | None
    linkedin_url: str | None
    lead_score: int
    priority: str
    verification_status: str
    email_valid: bool
    website_valid: bool
    is_duplicate: bool
    data_completeness: int
    quality_score: int
    quality_label: str
    score_reasons: list[ScoreReason]
    quality_flags: list[str]
    source: str
    created_at: datetime
    updated_at: datetime


class Filters(BaseModel):
    search: str = Field('', max_length=160)
    industry: str | None = Field(None, max_length=80)
    location: str | None = Field(None, max_length=80)
    min_score: int = Field(0, ge=0, le=100)
    max_score: int = Field(100, ge=0, le=100)
    priority: Literal['High', 'Medium', 'Low'] | None = None
    verification_status: Literal['Format Valid', 'Needs Review'] | None = None


class LeadsPage(BaseModel):
    items: list[LeadOut]
    total: int
    offset: int
    limit: int


class StatsOut(BaseModel):
    total: int
    high_priority: int
    format_valid: int
    externally_verified: int = 0
    average_score: float
    average_quality: float
    needs_review: int
    duplicates_prevented: int
    priorities: dict[str, int]
    industries: dict[str, int]


class DuplicateOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    incoming_company: str
    matched_lead_id: int
    reason: str
