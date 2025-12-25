from typing import List, Dict, Optional
from uuid import uuid4
from pydantic import BaseModel, Field

class DoctorNotes(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()), description="Unique identifier for the notes")
    history: Dict[str, str] = Field(default_factory=dict, description="Patient's medical history")
    medications: List[str] = Field(default_factory=list, description="List of medications")
    vitals: Dict[str, Optional[float]] = Field(default_factory=dict, description="Vital signs with their values")
    observations: Dict[str, str] = Field(default_factory=dict, description="Medical observations")
    symptoms: List[str] = Field(default_factory=list, description="List of symptoms")
    recommendations: List[str] = Field(default_factory=list, description="Medical recommendations")