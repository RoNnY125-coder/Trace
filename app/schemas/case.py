from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field, field_validator

class CaseBase(BaseModel):
    case_number: str = Field(..., min_length=1, description="Unique case code or identifier")
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = "ACTIVE"

    @field_validator("case_number")
    @classmethod
    def validate_case_number(cls, v: str) -> str:
        s = v.strip()
        if not s:
            raise ValueError("Case number cannot be empty or whitespace only.")
        return s

class CaseCreate(CaseBase):
    pass

class CaseUpdate(BaseModel):
    case_number: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None

class CaseResponse(CaseBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
