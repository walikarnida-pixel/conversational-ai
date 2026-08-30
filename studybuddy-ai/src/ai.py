"""Optional AI upgrade.

If a student adds an OPENAI_API_KEY (see .env.example) AND installs `openai`, the app can
ask a real model for richer flashcards. Without a key it stays fully offline and uses the
built-in generator — so the app ALWAYS works.
"""
import json
import os

try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "").strip()
IS_ONLINE = bool(OPENAI_API_KEY)


def mode_label():
    return "AI mode (real model)" if IS_ONLINE else "Offline mode (built-in generator)"


def ai_flashcards(text, n=8):
    """Return a list of {question, answer} from a real model, or None if unavailable."""
    if not IS_ONLINE:
        return None
    try:
        from openai import OpenAI
        client = OpenAI(api_key=OPENAI_API_KEY)
        prompt = (f"Create {n} exam flashcards from the notes below. "
                  f'Return ONLY JSON: {{"cards":[{{"question":"...","answer":"..."}}]}}.\n\n{text}')
        resp = client.chat.completions.create(
            model=os.getenv("MODEL_NAME", "gpt-4o-mini"),
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
            temperature=0.4,
        )
        data = json.loads(resp.choices[0].message.content)
        cards = data.get("cards", [])
        return [c for c in cards if c.get("question") and c.get("answer")] or None
    except Exception as e:
        print(f"[ai] falling back to offline generator: {e}")
        return None
