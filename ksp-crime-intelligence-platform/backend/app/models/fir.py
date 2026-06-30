from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from app.models.enums import CaseStatus, CrimeCategory
from app.models.location import Location


class Incident(BaseModel):
    """
    The atomic crime event. An FIR wraps one or more incidents in rare
    multi-offense filings, but in the common case FIR:Incident is 1:1.
    Kept separate from FIR so analytics_engine can query incidents directly
    without pulling full FIR paperwork metadata.
    """

    incident_id: Optional[str] = None
    fir_id: Optional[str] = None
    category: CrimeCategory
    sub_category: Optional[str] = None
    occurred_at: datetime
    reported_at: datetime
    location: Location
    mo_tags: list[str] = Field(default_factory=list)
    weapon_used: Optional[str] = None
    suspect_ids: list[str] = Field(default_factory=list)
    victim_ids: list[str] = Field(default_factory=list)
    narrative_summary: Optional[str] = None


class FIR(BaseModel):
    fir_id: Optional[str] = None
    fir_number: str = Field(..., description="Official KSP FIR number, e.g. 0123/2026")
    police_station: str
    district: str
    filed_by_officer_id: str
    status: CaseStatus = CaseStatus.OPEN
    filed_at: datetime
    last_updated_at: Optional[datetime] = None
    incident: Incident
    evidence_file_ids: list[str] = Field(
        default_factory=list, description="Stratus object keys"
    )
    priority_score: Optional[float] = Field(default=None, ge=0, le=1)
    raw_ocr_text: Optional[str] = Field(
        default=None,
        description="Populated by ocr_document_intel function for scanned FIRs",
    )
