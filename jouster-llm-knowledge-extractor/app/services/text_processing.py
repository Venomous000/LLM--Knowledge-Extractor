
import re
import nltk
from collections import Counter
from typing import List

def _ensure_nltk():
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt')
    try:
        nltk.data.find('taggers/averaged_perceptron_tagger')
    except LookupError:
        nltk.download('averaged_perceptron_tagger')
    try:
        nltk.data.find('corpora/stopwords')
    except LookupError:
        nltk.download('stopwords')

_ensure_nltk()
from nltk import word_tokenize, pos_tag
from nltk.corpus import stopwords

STOPWORDS = set(stopwords.words('english'))

SENT_POSITIVE = set("""good great excellent positive success benefit happy love
    effective improve improved improving robust secure scalable reliable""".split())
SENT_NEGATIVE = set("""bad poor negative issue bug failure fail failing broken
    insecure slow unreliable problem""".split())

def split_sentences(text: str) -> List[str]:
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    return [s.strip() for s in sentences if s.strip()]

def summarize(text: str, max_sentences: int = 2) -> str:
    sentences = split_sentences(text)
    return " ".join(sentences[:max_sentences]) if sentences else ""

def extract_noun_keywords(text: str, k: int = 3) -> List[str]:
    tokens = [t.lower() for t in word_tokenize(text) if re.match(r"[A-Za-z\-']+$", t)]
    tokens = [t for t in tokens if t not in STOPWORDS]
    tagged = pos_tag(tokens)
    nouns = [w for (w, tag) in tagged if tag.startswith('NN')]
    counts = Counter(nouns)
    return [w for (w, _) in counts.most_common(k)]

def sentiment_heuristic(text: str) -> str:
    tokens = set([t.lower() for t in re.findall(r"[A-Za-z]+", text)])
    pos = len(tokens & SENT_POSITIVE)
    neg = len(tokens & SENT_NEGATIVE)
    if pos > neg:
        return "positive"
    if neg > pos:
        return "negative"
    return "neutral"

def extract_topics(text: str, k: int = 3) -> List[str]:
    return extract_noun_keywords(text, k=k)

def confidence_heuristic(text: str, keywords: List[str], llm_ok: bool) -> float:
    length_factor = min(len(text) / 800.0, 1.0)
    coverage = min(len(keywords) / 3.0, 1.0)
    bonus = 0.15 if llm_ok else 0.0
    return round(min(1.0, 0.5 * length_factor + 0.35 * coverage + bonus), 2)
