
from typing import Dict, Any
from app.config import TOPIC_COUNT, KEYWORD_COUNT
from app.services.llm_client import summarize_with_llm
from app.services.text_processing import (
    extract_noun_keywords, extract_topics, sentiment_heuristic, confidence_heuristic
)

def analyze_text(text: str, title: str | None = None) -> Dict[str, Any]:
    summary, provider, llm_ok = summarize_with_llm(text)
    keywords = extract_noun_keywords(text, k=KEYWORD_COUNT)
    topics = extract_topics(text, k=TOPIC_COUNT)
    sentiment = sentiment_heuristic(text)
    confidence = confidence_heuristic(text, keywords, llm_ok)
    return {
        "title": title,
        "summary": summary,
        "topics": topics,
        "sentiment": sentiment,
        "keywords": keywords,
        "confidence": int(round(confidence * 100)),
        "llm_provider": provider,
        "llm_error": int(not llm_ok),
    }
