
from typing import Tuple
from app.config import OPENAI_API_KEY, SUMMARY_SENTENCE_MAX
from app.services.text_processing import summarize

_client = None
def _get_client():
    global _client
    if _client is None:
        if OPENAI_API_KEY:
            try:
                from openai import OpenAI
                _client = OpenAI(api_key=OPENAI_API_KEY)
            except Exception:
                _client = None
        else:
            _client = None
    return _client

def summarize_with_llm(text: str) -> Tuple[str, str, bool]:
    client = _get_client()
    if client is None:
        return summarize(text, SUMMARY_SENTENCE_MAX), "mock", False

    try:
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Summarize the user's text in 1-2 sentences."},
                {"role": "user", "content": text},
            ],
            temperature=0.2,
            max_tokens=120,
        )
        content = resp.choices[0].message.content.strip()
        return content, "openai:gpt-4o-mini", True
    except Exception:
        return summarize(text, SUMMARY_SENTENCE_MAX), "mock", False
