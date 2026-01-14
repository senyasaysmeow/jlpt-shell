#!/usr/bin/env python3
"""JLPT Terminal Greeting - Displays a random JLPT vocabulary word."""

import json
import os
import random
import urllib.request

# Configuration

JLPT_LEVEL = random.choice(["N5", "N4", "N3", "N2", "N1"])
CACHE_DIR = os.path.expanduser("~/.cache/jlpt-greeting")
SHOWN_FILE = os.path.join(CACHE_DIR, f"shown_{JLPT_LEVEL}.txt")

# Colors
YELLOW = "\033[1;33m"
MAGENTA = "\033[1;35m"
GREEN = "\033[1;32m"
BLUE = "\033[1;34m"
DIM = "\033[2m"
RED = "\033[0;31m"
RESET = "\033[0m"


def fetch_word():
    """Fetch a random JLPT word from jisho.org."""
    page = random.randint(1, 10)
    url = f"https://jisho.org/api/v1/search/words?keyword=%23jlpt-{JLPT_LEVEL.lower()}&page={page}"
    
    try:
        with urllib.request.urlopen(url, timeout=5) as response:
            return json.loads(response.read().decode())
    except Exception:
        return None


def load_shown_words() -> set:
    """Load previously shown words."""
    if os.path.exists(SHOWN_FILE):
        with open(SHOWN_FILE, "r") as f:
            return set(line.strip() for line in f)
    return set()


def mark_shown(slug: str):
    """Mark a word as shown."""
    with open(SHOWN_FILE, "a") as f:
        f.write(slug + "\n")


def display_word(data: dict):
    """Display a random word from the fetched data."""
    if not data or "data" not in data or not data["data"]:
        print(f"{RED}No vocabulary found.{RESET}")
        return

    words = data["data"]
    shown = load_shown_words()
    available = [w for w in words if w.get("slug", "") not in shown]

    # Reset if all shown
    if not available:
        if os.path.exists(SHOWN_FILE):
            os.remove(SHOWN_FILE)
        available = words

    word = random.choice(available)

    # Extract info
    jp = word.get("japanese", [{}])[0]
    kanji = jp.get("word", jp.get("reading", "N/A"))
    reading = jp.get("reading", "")
    senses = word.get("senses", [{}])
    meanings = []
    for sense in senses:
        meanings.extend(sense.get("english_definitions", [])[:3])
    meaning_str = ", ".join(meanings[:5])
    pos = senses[0].get("parts_of_speech", [""])[0] if senses else ""

    mark_shown(word.get("slug", kanji))

    # Display
    print()
    print(f"{YELLOW}📚 JLPT Word of the Session{RESET}")
    print(f"{MAGENTA}{kanji}{RESET}", end="")
    if reading and reading != kanji:
        print(f"  {GREEN}({reading}){RESET}")
    else:
        print()
    print(f"{BLUE}{meaning_str}{RESET}")
    if pos:
        print(f"{DIM}{pos} {JLPT_LEVEL}{RESET}")
    print()


def main():
    os.makedirs(CACHE_DIR, exist_ok=True)
    data = fetch_word()
    if data:
        display_word(data)
    else:
        print(f"{RED}Could not fetch JLPT vocabulary. Check your internet connection.{RESET}")


if __name__ == "__main__":
    main()
