import os
import json
import importlib.util
from pathlib import Path

import requests

BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]
API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
STATE_FILE = Path(__file__).parent / "state.json"
POSTS_FILE = Path(__file__).parent / "posts.py"


def load_state():
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    return {"index": 0}


def save_state(state):
    STATE_FILE.write_text(json.dumps(state, ensure_ascii=False), encoding="utf-8")


def load_posts():
    spec = importlib.util.spec_from_file_location("posts", POSTS_FILE)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.POSTS


def send_message(text):
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": False,
    }
    resp = requests.post(API_URL, json=payload, timeout=15)
    resp.raise_for_status()
    return resp.json()


def main():
    posts = load_posts()
    state = load_state()
    idx = state["index"]

    if idx >= len(posts):
        idx = 0

    post = posts[idx]
    text = f"<b>{post['title']}</b>\n\n{post['text']}"
    result = send_message(text)
    print(f"Sent day {post['day']}: {post['title']} — {result.get('ok')}")

    state["index"] = idx + 1
    save_state(state)


if __name__ == "__main__":
    main()
