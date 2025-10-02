
from app.services.analyzer import analyze_text

def test_analyze_text_basic():
    text = "Jouster releases a new LLM extractor. It is robust and scalable. Users love the reliability."
    result = analyze_text(text, title="News")
    assert result["summary"]
    assert result["sentiment"] in ("positive","neutral","negative")
    assert len(result["keywords"]) <= 3
    assert len(result["topics"]) <= 3
    assert 0 <= result["confidence"] <= 100
