import os
import importlib.util
from datetime import date, datetime
from pathlib import Path

import requests

BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]
API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
POSTS_FILE = Path(__file__).parent / "posts.py"

FIRST_POST_DATE = date(2026, 5, 31)


def load_posts():
    spec = importlib.util.spec_from_file_location("posts", POSTS_FILE)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.POSTS


def get_today_index(posts):
    delta = date.today() - FIRST_POST_DATE
    days = delta.days
    if days < 0:
        days = 0
    return days % len(posts)


def send_message(text):
    resp = requests.post(
        API_URL,
        json={"chat_id": CHAT_ID, "text": text, "parse_mode": "HTML"},
        timeout=15,
    )
    resp.raise_for_status()
    return resp.json()


def main():
    posts = load_posts()
    idx = get_today_index(posts)
    post = posts[idx]
    text = f"<b>{post['title']}</b>\n\n{post['text']}"
    result = send_message(text)
    print(f"Sent [{idx+1}/{len(posts)}] day {post['day']}: {post['title']} — {result.get('ok')}")


if __name__ == "__main__":
    main()
