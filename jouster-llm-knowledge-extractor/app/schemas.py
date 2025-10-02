
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class AnalyzeRequest(BaseModel):
    text: str = Field(..., min_length=1)
    title: Optional[str] = None

class AnalyzeBatchItem(BaseModel):
    text: str = Field(..., min_length=1)
    title: Optional[str] = None

class AnalyzeBatchRequest(BaseModel):
    items: List[AnalyzeBatchItem]

class AnalysisOut(BaseModel):
    id: int
    title: Optional[str]
    summary: str
    topics: List[str]
    sentiment: str
    keywords: List[str]
    confidence: float
    llm_provider: str
    llm_error: bool
    created_at: datetime

    class Config:
        from_attributes = True
