"""StudyBuddy core — turn study notes into flashcards and a quiz.

This works fully OFFLINE (no API key) using simple, explainable text rules, so every
student can run it. `src/ai.py` can optionally upgrade the output with a real AI model.
"""
import random
import re

_STOP = {
    "the", "a", "an", "is", "are", "was", "were", "be", "been", "being", "of", "to", "in",
    "on", "for", "and", "or", "but", "with", "as", "by", "at", "from", "that", "this", "these",
    "those", "it", "its", "into", "than", "then", "which", "who", "whom", "can", "will", "also",
    "such", "used", "use", "using", "have", "has", "had", "their", "they", "them", "you", "your",
}


def _sentences(text):
    """Split notes into clean sentences."""
    raw = re.split(r"(?<=[.!?])\s+|\n+", text or "")
    return [s.strip() for s in raw if len(s.strip().split()) >= 4]


def _key_term(sentence):
    """Pick the most 'quiz-worthy' word in a sentence: prefer a capitalised term,
    else the longest non-stopword word."""
    words = re.findall(r"[A-Za-z][A-Za-z\-]+", sentence)
    caps = [w for w in words[1:] if w[0].isupper()]      # skip the first word (sentence start)
    pool = caps or [w for w in words if w.lower() not in _STOP and len(w) > 4]
    if not pool:
        return None
    return max(pool, key=len)


def make_flashcards(text, n=8):
    """Fill-in-the-blank flashcards: hide the key term in each sentence."""
    cards = []
    for s in _sentences(text):
        term = _key_term(s)
        if not term:
            continue
        question = re.sub(r"\b" + re.escape(term) + r"\b", "_____", s, count=1)
        if "_____" in question:
            cards.append({"question": question, "answer": term})
        if len(cards) >= n:
            break
    return cards


def make_quiz(text, n=5, seed=None):
    """Multiple-choice quiz built from the flashcards (4 options each)."""
    rng = random.Random(seed)
    cards = make_flashcards(text, n=50)
    all_terms = list({c["answer"] for c in cards})
    quiz = []
    for c in cards:
        correct = c["answer"]
        distractors = [t for t in all_terms if t != correct]
        rng.shuffle(distractors)
        options = [correct] + distractors[:3]
        while len(options) < 4:                          # pad if the notes are short
            options.append("None of the above")
        rng.shuffle(options)
        quiz.append({"question": c["question"], "options": options, "answer": correct})
        if len(quiz) >= n:
            break
    return quiz


def score_quiz(quiz, answers):
    """answers: list of chosen option strings. Returns (correct_count, total)."""
    correct = sum(1 for q, a in zip(quiz, answers) if a == q["answer"])
    return correct, len(quiz)
