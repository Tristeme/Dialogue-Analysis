from transformers import pipeline
import re
import spacy

# HuggingFace sentiment-analysis pipeline
classifier = pipeline(model="distilbert/distilbert-base-uncased-finetuned-sst-2-english")

# filler words list
FILLER_WORDS = ["um", "like", "you know", "uh", "actually", "basically"]

# spaCy english model
nlp = spacy.load("en_core_web_sm")

# Return sentiment label: POSITIVE / NEGATIVE / NEUTRAL
def compute_sentiment(text):
    result = classifier(text)[0]
    label = result['label'].lower()
    score = round(result['score'], 3)
    return label, score

# Filler-word ratio (number of filler words ÷ total words) via spaCy or regular expressions
def compute_filler_ratio(text):
    doc = nlp(text.lower())
    words = [token.text for token in doc if token.is_alpha]
    total_words = len(words)
    # doc: hey, um, how was your weekend?
    # words: ['hey', 'um', 'how', 'was', 'your', 'weekend']
    filler_count = sum(1 for word in words if word in FILLER_WORDS)
    return round(filler_count / total_words, 3) if total_words > 0 else 0.0
