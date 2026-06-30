from datetime import date
from typing import Optional

from pydantic import BaseModel, Field


class PersonBase(BaseModel):
    person_id: Optional[str] = None
    full_name: str
    aliases: list[str] = Field(default_factory=list)
    date_of_birth: Optional[date] = None
    gender: Optional[str] = None
    phone_numbers: list[str] = Field(default_factory=list)
    address_text: Optional[str] = None
    id_proof_number: Optional[str] = None  # Aadhaar/PAN/etc, store hashed at rest


class Suspect(PersonBase):
    known_mo: list[str] = Field(
        default_factory=list, description="Tags describing modus operandi"
    )
    prior_case_ids: list[str] = Field(default_factory=list)
    risk_score: Optional[float] = Field(default=None, ge=0, le=1)
    is_repeat_offender: bool = False


class Victim(PersonBase):
    incident_ids: list[str] = Field(default_factory=list)
    is_vulnerable: bool = (
        False  # e.g. minor, elderly — drives sensitivity handling in UI
    )
