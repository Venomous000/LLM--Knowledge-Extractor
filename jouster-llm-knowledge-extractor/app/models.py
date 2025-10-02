
from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from sqlalchemy.types import JSON
from app.database import Base

class Analysis(Base):
    __tablename__ = "analyses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(512), nullable=True)
    text = Column(Text, nullable=False)
    summary = Column(Text, nullable=False)
    topics = Column(JSON, nullable=False)
    sentiment = Column(String(16), nullable=False)
    keywords = Column(JSON, nullable=False)
    confidence = Column(Integer, nullable=False)  # 0..100
    llm_provider = Column(String(64), nullable=False)
    llm_error = Column(Integer, nullable=False, default=0)  # 0/1
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
