"""StudyBuddy AI — turn your notes into flashcards and a quiz.

Run it:   streamlit run app.py
Works offline (no API key needed).
"""
import streamlit as st

from src import ai
from src.generator import make_flashcards, make_quiz, score_quiz

st.set_page_config(page_title="StudyBuddy AI", page_icon="📚", layout="centered")

# ---- load sample notes so the app is useful on first run --------------------
try:
    with open("data/sample_notes.txt", encoding="utf-8") as f:
        SAMPLE = f.read()
except FileNotFoundError:
    SAMPLE = "Photosynthesis is the process by which plants make food using sunlight."

st.title("📚 StudyBuddy AI")
st.caption("Paste your notes and get instant flashcards and a quiz. Great for exam revision!")

with st.sidebar:
    st.header("How it works")
    st.write(f"**Mode:** {ai.mode_label()}")
    st.write("1. Paste notes.\n2. Pick how many cards/questions.\n3. Generate and study!")
    st.caption("Add an OpenAI key in `.env` for AI-enhanced cards. Not required.")

notes = st.text_area("Your study notes:", value=SAMPLE, height=180)
c1, c2 = st.columns(2)
n_cards = c1.slider("Flashcards", 3, 15, 6)
n_quiz = c2.slider("Quiz questions", 3, 10, 5)

tab_cards, tab_quiz = st.tabs(["🃏 Flashcards", "❓ Quiz"])

# ---- Flashcards -------------------------------------------------------------
with tab_cards:
    if st.button("Generate flashcards", type="primary"):
        cards = ai.ai_flashcards(notes, n_cards) or make_flashcards(notes, n_cards)
        if not cards:
            st.warning("Please paste a few more sentences of notes.")
        for i, c in enumerate(cards, 1):
            with st.expander(f"Card {i}: {c['question']}"):
                st.success(f"Answer: **{c['answer']}**")

# ---- Quiz -------------------------------------------------------------------
with tab_quiz:
    if "quiz" not in st.session_state:
        st.session_state.quiz = None
    if st.button("Generate quiz", type="primary"):
        st.session_state.quiz = make_quiz(notes, n_quiz, seed=42)

    quiz = st.session_state.quiz
    if quiz:
        with st.form("quiz_form"):
            answers = []
            for i, q in enumerate(quiz, 1):
                answers.append(st.radio(f"Q{i}. {q['question']}", q["options"], key=f"q{i}"))
            submitted = st.form_submit_button("Check answers")
        if submitted:
            correct, total = score_quiz(quiz, answers)
            st.metric("Your score", f"{correct} / {total}")
            for i, (q, a) in enumerate(zip(quiz, answers), 1):
                mark = "✅" if a == q["answer"] else "❌"
                st.write(f"{mark} Q{i}: correct answer is **{q['answer']}**")

st.divider()
st.caption("Open `src/generator.py` to see how it works · run `pytest` to test it · see README for the lab.")
