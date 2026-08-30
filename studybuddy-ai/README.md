# 📚 StudyBuddy AI

Paste your study notes → get instant **flashcards** and a **quiz**. Perfect for exam revision.
Runs **offline** (no API key needed), so it works on any laptop.

## Quick start (easiest)
- **Windows:** double-click **`run.bat`**
- **macOS/Linux:** in a terminal, run **`./run.sh`**

The browser opens at `http://localhost:8501`. That's it.

## Manual start (if you prefer)
```bash
python -m venv venv
# Windows:  venv\Scripts\activate
# macOS:    source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Run the tests
```bash
pytest -v
```

## Project structure
```
studybuddy-ai/
  app.py                 # the Streamlit app (UI)
  src/generator.py       # makes flashcards + quiz (offline logic)
  src/ai.py              # optional AI upgrade if you add a key
  data/sample_notes.txt  # example notes
  tests/test_generator.py
  requirements.txt · run.bat · run.sh · README.md
```

## Ideas to extend (Day 8)
- Add a **"Summary" tab** that shortens the notes into 5 bullet points.
- Let users **upload a .txt file** of notes.
- Add **difficulty levels** (easy = fill-in-the-blank, hard = MCQ).

See the workshop PDF for the full Day 8 & Day 9 tasks.
