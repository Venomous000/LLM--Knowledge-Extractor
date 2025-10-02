
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import Base, engine, get_db
from app import models
from app.schemas import AnalyzeRequest, AnalysisOut, AnalyzeBatchRequest
from app.services.analyzer import analyze_text

Base.metadata.create_all(bind=engine)
router = APIRouter()

@router.post("/analyze", response_model=AnalysisOut)
def analyze(req: AnalyzeRequest, db: Session = Depends(get_db)):
    text = (req.text or "").strip()
    if not text:
        raise HTTPException(status_code=400, detail="text must not be empty")

    result = analyze_text(text, title=req.title)
    obj = models.Analysis(
        title=result["title"],
        text=text,
        summary=result["summary"],
        topics=result["topics"],
        sentiment=result["sentiment"],
        keywords=result["keywords"],
        confidence=result["confidence"],
        llm_provider=result["llm_provider"],
        llm_error=result["llm_error"],
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)

    return {
        "id": obj.id,
        "title": obj.title,
        "summary": obj.summary,
        "topics": obj.topics,
        "sentiment": obj.sentiment,
        "keywords": obj.keywords,
        "confidence": round(obj.confidence / 100.0, 2),
        "llm_provider": obj.llm_provider,
        "llm_error": bool(obj.llm_error),
        "created_at": obj.created_at,
    }

@router.post("/analyze/batch", response_model=List[AnalysisOut])
def analyze_batch(req: AnalyzeBatchRequest, db: Session = Depends(get_db)):
    outputs = []
    for item in req.items:
        text = (item.text or "").strip()
        if not text:
            continue
        result = analyze_text(text, title=item.title)
        obj = models.Analysis(
            title=result["title"],
            text=text,
            summary=result["summary"],
            topics=result["topics"],
            sentiment=result["sentiment"],
            keywords=result["keywords"],
            confidence=result["confidence"],
            llm_provider=result["llm_provider"],
            llm_error=result["llm_error"],
        )
        db.add(obj)
        db.flush()
        outputs.append(obj)
    db.commit()

    return [{
        "id": o.id,
        "title": o.title,
        "summary": o.summary,
        "topics": o.topics,
        "sentiment": o.sentiment,
        "keywords": o.keywords,
        "confidence": round(o.confidence / 100.0, 2),
        "llm_provider": o.llm_provider,
        "llm_error": bool(o.llm_error),
        "created_at": o.created_at,
    } for o in outputs]

@router.get("/search", response_model=List[AnalysisOut])
def search(topic: str, db: Session = Depends(get_db)):
    all_items = db.query(models.Analysis).order_by(models.Analysis.created_at.desc()).all()
    topic_lower = topic.strip().lower()
    results = []
    for o in all_items:
        topics = [t.lower() for t in (o.topics or [])]
        keywords = [k.lower() for k in (o.keywords or [])]
        if topic_lower in topics or topic_lower in keywords:
            results.append({
                "id": o.id,
                "title": o.title,
                "summary": o.summary,
                "topics": o.topics,
                "sentiment": o.sentiment,
                "keywords": o.keywords,
                "confidence": round(o.confidence / 100.0, 2),
                "llm_provider": o.llm_provider,
                "llm_error": bool(o.llm_error),
                "created_at": o.created_at,
            })
    return results
