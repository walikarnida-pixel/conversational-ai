"""Tests for StudyBuddy (Day 9: AI-assisted testing). Run:  pytest -v"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.generator import make_flashcards, make_quiz, score_quiz

NOTES = ("Photosynthesis is the process by which plants make food using sunlight. "
         "Chlorophyll is the green pigment in leaves. "
         "An algorithm is a step by step set of instructions to solve a problem.")


def test_flashcards_are_created():
    cards = make_flashcards(NOTES, n=5)
    assert len(cards) >= 1
    assert all("_____" in c["question"] for c in cards)
    assert all(c["answer"] for c in cards)


def test_quiz_has_four_options_including_answer():
    quiz = make_quiz(NOTES, n=3, seed=1)
    assert len(quiz) >= 1
    for q in quiz:
        assert len(q["options"]) == 4
        assert q["answer"] in q["options"]


def test_scoring_counts_correct_answers():
    quiz = make_quiz(NOTES, n=3, seed=1)
    perfect = [q["answer"] for q in quiz]
    correct, total = score_quiz(quiz, perfect)
    assert correct == total


def test_empty_notes_do_not_crash():
    assert make_flashcards("", n=5) == []
    assert make_quiz("", n=5) == []
