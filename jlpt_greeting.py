#!/usr/bin/env python3
"""JLPT Quiz - Interactive Anki-style quiz for JLPT vocabulary."""

import argparse
import json
import os
import random
import urllib.request
from datetime import datetime

# Configuration

CACHE_DIR = os.path.expanduser("~/.cache/jlpt-quiz")

# Colors
YELLOW = "\033[1;33m"
MAGENTA = "\033[1;35m"
GREEN = "\033[1;32m"
BLUE = "\033[1;34m"
CYAN = "\033[1;36m"
DIM = "\033[2m"
RED = "\033[0;31m"
RESET = "\033[0m"

# Romaji conversion tables
HIRAGANA_TO_ROMAJI = {
    'あ': 'a', 'い': 'i', 'う': 'u', 'え': 'e', 'お': 'o',
    'か': 'ka', 'き': 'ki', 'く': 'ku', 'け': 'ke', 'こ': 'ko',
    'が': 'ga', 'ぎ': 'gi', 'ぐ': 'gu', 'げ': 'ge', 'ご': 'go',
    'さ': 'sa', 'し': 'shi', 'す': 'su', 'せ': 'se', 'そ': 'so',
    'ざ': 'za', 'じ': 'ji', 'ず': 'zu', 'ぜ': 'ze', 'ぞ': 'zo',
    'た': 'ta', 'ち': 'chi', 'つ': 'tsu', 'て': 'te', 'と': 'to',
    'だ': 'da', 'ぢ': 'ji', 'づ': 'zu', 'で': 'de', 'ど': 'do',
    'な': 'na', 'に': 'ni', 'ぬ': 'nu', 'ね': 'ne', 'の': 'no',
    'は': 'ha', 'ひ': 'hi', 'ふ': 'fu', 'へ': 'he', 'ほ': 'ho',
    'ば': 'ba', 'び': 'bi', 'ぶ': 'bu', 'べ': 'be', 'ぼ': 'bo',
    'ぱ': 'pa', 'ぴ': 'pi', 'ぷ': 'pu', 'ぺ': 'pe', 'ぽ': 'po',
    'ま': 'ma', 'み': 'mi', 'む': 'mu', 'め': 'me', 'も': 'mo',
    'や': 'ya', 'ゆ': 'yu', 'よ': 'yo',
    'ら': 'ra', 'り': 'ri', 'る': 'ru', 'れ': 're', 'ろ': 'ro',
    'わ': 'wa', 'ゐ': 'wi', 'ゑ': 'we', 'を': 'wo', 'ん': 'n',
    'きゃ': 'kya', 'きゅ': 'kyu', 'きょ': 'kyo',
    'ぎゃ': 'gya', 'ぎゅ': 'gyu', 'ぎょ': 'gyo',
    'しゃ': 'sha', 'しゅ': 'shu', 'しょ': 'sho',
    'じゃ': 'ja', 'じゅ': 'ju', 'じょ': 'jo',
    'ちゃ': 'cha', 'ちゅ': 'chu', 'ちょ': 'cho',
    'にゃ': 'nya', 'にゅ': 'nyu', 'にょ': 'nyo',
    'ひゃ': 'hya', 'ひゅ': 'hyu', 'ひょ': 'hyo',
    'びゃ': 'bya', 'びゅ': 'byu', 'びょ': 'byo',
    'ぴゃ': 'pya', 'ぴゅ': 'pyu', 'ぴょ': 'pyo',
    'みゃ': 'mya', 'みゅ': 'myu', 'みょ': 'myo',
    'りゃ': 'rya', 'りゅ': 'ryu', 'りょ': 'ryo',
    'ー': '', 'っ': '',
}

KATAKANA_TO_ROMAJI = {
    'ア': 'a', 'イ': 'i', 'ウ': 'u', 'エ': 'e', 'オ': 'o',
    'カ': 'ka', 'キ': 'ki', 'ク': 'ku', 'ケ': 'ke', 'コ': 'ko',
    'ガ': 'ga', 'ギ': 'gi', 'グ': 'gu', 'ゲ': 'ge', 'ゴ': 'go',
    'サ': 'sa', 'シ': 'shi', 'ス': 'su', 'セ': 'se', 'ソ': 'so',
    'ザ': 'za', 'ジ': 'ji', 'ズ': 'zu', 'ゼ': 'ze', 'ゾ': 'zo',
    'タ': 'ta', 'チ': 'chi', 'ツ': 'tsu', 'テ': 'te', 'ト': 'to',
    'ダ': 'da', 'ヂ': 'ji', 'ヅ': 'zu', 'デ': 'de', 'ド': 'do',
    'ナ': 'na', 'ニ': 'ni', 'ヌ': 'nu', 'ネ': 'ne', 'ノ': 'no',
    'ハ': 'ha', 'ヒ': 'hi', 'フ': 'fu', 'ヘ': 'he', 'ホ': 'ho',
    'バ': 'ba', 'ビ': 'bi', 'ブ': 'bu', 'ベ': 'be', 'ボ': 'bo',
    'パ': 'pa', 'ピ': 'pi', 'プ': 'pu', 'ペ': 'pe', 'ポ': 'po',
    'マ': 'ma', 'ミ': 'mi', 'ム': 'mu', 'メ': 'me', 'モ': 'mo',
    'ヤ': 'ya', 'ユ': 'yu', 'ヨ': 'yo',
    'ラ': 'ra', 'リ': 'ri', 'ル': 'ru', 'レ': 're', 'ロ': 'ro',
    'ワ': 'wa', 'ヰ': 'wi', 'ヱ': 'we', 'ヲ': 'wo', 'ン': 'n',
    'キャ': 'kya', 'キュ': 'kyu', 'キョ': 'kyo',
    'ギャ': 'gya', 'ギュ': 'gyu', 'ギョ': 'gyo',
    'シャ': 'sha', 'シュ': 'shu', 'ショ': 'sho',
    'ジャ': 'ja', 'ジュ': 'ju', 'ジョ': 'jo',
    'チャ': 'cha', 'チュ': 'chu', 'チョ': 'cho',
    'ニャ': 'nya', 'ニュ': 'nyu', 'ニョ': 'nyo',
    'ヒャ': 'hya', 'ヒュ': 'hyu', 'ヒョ': 'hyo',
    'ビャ': 'bya', 'ビュ': 'byu', 'ビョ': 'byo',
    'ピャ': 'pya', 'ピュ': 'pyu', 'ピョ': 'pyo',
    'ミャ': 'mya', 'ミュ': 'myu', 'ミョ': 'myo',
    'リャ': 'rya', 'リュ': 'ryu', 'リョ': 'ryo',
    'ー': '', 'ッ': '',
}


def kana_to_romaji(text: str) -> str:
    """Convert hiragana/katakana to romaji."""
    result = []
    i = 0
    text_len = len(text)
    
    while i < text_len:
        # Try two-character combinations first
        if i + 1 < text_len:
            two_char = text[i:i+2]
            if two_char in HIRAGANA_TO_ROMAJI:
                result.append(HIRAGANA_TO_ROMAJI[two_char])
                i += 2
                continue
            if two_char in KATAKANA_TO_ROMAJI:
                result.append(KATAKANA_TO_ROMAJI[two_char])
                i += 2
                continue
        
        # Try single character
        char = text[i]
        if char in HIRAGANA_TO_ROMAJI:
            romaji = HIRAGANA_TO_ROMAJI[char]
            # Handle small tsu (っ/ッ) by doubling next consonant
            if char in ('っ', 'ッ') and i + 1 < text_len:
                next_char = text[i + 1]
                next_romaji = HIRAGANA_TO_ROMAJI.get(next_char, KATAKANA_TO_ROMAJI.get(next_char, ''))
                if next_romaji:
                    result.append(next_romaji[0])
            else:
                result.append(romaji)
        elif char in KATAKANA_TO_ROMAJI:
            romaji = KATAKANA_TO_ROMAJI[char]
            if char in ('っ', 'ッ') and i + 1 < text_len:
                next_char = text[i + 1]
                next_romaji = HIRAGANA_TO_ROMAJI.get(next_char, KATAKANA_TO_ROMAJI.get(next_char, ''))
                if next_romaji:
                    result.append(next_romaji[0])
            else:
                result.append(romaji)
        else:
            result.append(char)
        i += 1
    
    return ''.join(result)


def normalize_romaji(text: str) -> str:
    """Normalize romaji for flexible matching."""
    text = text.lower().strip()
    # Handle common variations
    text = text.replace('ō', 'ou').replace('ū', 'uu').replace('ā', 'aa')
    text = text.replace('ē', 'ee').replace('ī', 'ii')
    # Remove spaces and hyphens
    text = text.replace(' ', '').replace('-', '')
    return text


def get_cache_file(level: str, cache_type: str) -> str:
    """Get cache file path for a given level and type."""
    return os.path.join(CACHE_DIR, f"{cache_type}_{level}.json")


def load_word_cache(level: str) -> list:
    """Load cached words for a given JLPT level."""
    cache_file = get_cache_file(level, "words")
    if os.path.exists(cache_file):
        try:
            with open(cache_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []


def save_word_cache(level: str, words: list):
    """Save words to cache for a given JLPT level."""
    cache_file = get_cache_file(level, "words")
    try:
        with open(cache_file, "w", encoding="utf-8") as f:
            json.dump(words, f, ensure_ascii=False, indent=2)
    except Exception:
        pass


def add_words_to_cache(level: str, new_words: list):
    """Add new words to cache, avoiding duplicates."""
    cached_words = load_word_cache(level)
    cached_slugs = {w.get("slug") for w in cached_words if w.get("slug")}
    
    for word in new_words:
        slug = word.get("slug")
        if slug and slug not in cached_slugs:
            cached_words.append(word)
            cached_slugs.add(slug)
    
    save_word_cache(level, cached_words)


def load_quiz_stats(level: str) -> dict:
    """Load quiz statistics for words."""
    stats_file = get_cache_file(level, "quiz_stats")
    if os.path.exists(stats_file):
        try:
            with open(stats_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}


def save_quiz_stats(level: str, stats: dict):
    """Save quiz statistics."""
    stats_file = get_cache_file(level, "quiz_stats")
    try:
        with open(stats_file, "w", encoding="utf-8") as f:
            json.dump(stats, f, ensure_ascii=False, indent=2)
    except Exception:
        pass


def update_quiz_stat(level: str, slug: str, correct: bool):
    """Update quiz statistics for a word."""
    stats = load_quiz_stats(level)
    
    if slug not in stats:
        stats[slug] = {"correct": 0, "incorrect": 0, "last_reviewed": None}
    
    if correct:
        stats[slug]["correct"] += 1
    else:
        stats[slug]["incorrect"] += 1
    
    stats[slug]["last_reviewed"] = datetime.now().isoformat()
    save_quiz_stats(level, stats)


def fetch_word(level: str):
    """Fetch JLPT words from jisho.org and cache them."""
    page = random.randint(1, 10)
    url = f"https://jisho.org/api/v1/search/words?keyword=%23jlpt-{level.lower()}&page={page}"
    
    try:
        with urllib.request.urlopen(url, timeout=5) as response:
            data = json.loads(response.read().decode())
            if data and "data" in data:
                # Add fetched words to cache
                add_words_to_cache(level, data["data"])
            return data
    except Exception:
        return None


def quiz_mode(level: str, use_cache_only: bool = False):
    """Run interactive quiz mode."""
    print(f"\n{YELLOW}🎯 JLPT Quiz Mode - {level}{RESET}")
    if use_cache_only:
        print(f"{DIM}(Offline mode - using cached words only){RESET}")
    print(f"{DIM}Type the romaji reading for each kanji. Type 'quit' to exit.{RESET}\n")
    
    cached_words = load_word_cache(level)
    
    if not use_cache_only:
        # Try to fetch new words in background
        fetch_word(level)
        cached_words = load_word_cache(level)
    
    if not cached_words:
        print(f"{RED}No cached words available. Please run in online mode first to download words.{RESET}")
        return
    
    stats = load_quiz_stats(level)
    correct_count = 0
    incorrect_count = 0
    
    while True:
        # Select word (prioritize words with fewer correct answers)
        word = select_quiz_word(cached_words, stats)
        
        if not word:
            print(f"{RED}No more words available.{RESET}")
            break
        
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
        slug = word.get("slug", "")
        
        # Convert reading to romaji
        expected_romaji = kana_to_romaji(reading)
        normalized_expected = normalize_romaji(expected_romaji)
        
        # Display question - ONLY KANJI first
        print(f"{CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}")
        print(f"{MAGENTA}{kanji}{RESET}")
        
        # First attempt
        try:
            user_input = input(f"\n{YELLOW}Romaji >{RESET} ").strip()
        except (EOFError, KeyboardInterrupt):
            print(f"\n{DIM}Quiz ended.{RESET}")
            break
        
        if user_input.lower() in ('quit', 'exit', 'q'):
            break
        
        # Check first answer
        normalized_input = normalize_romaji(user_input)
        
        if normalized_input == normalized_expected:
            print(f"{GREEN}✓ Correct!{RESET}")
            print(f"{BLUE}{meaning_str}{RESET}")
            if pos:
                print(f"{DIM}{pos} • {level}{RESET}")
            update_quiz_stat(level, slug, True)
            correct_count += 1
        else:
            # First attempt failed - show hint and give second try
            print(f"{RED}✗ Incorrect.{RESET}")
            print(f"{DIM}Hint - Meaning: {meaning_str}{RESET}")
            
            # Second attempt
            try:
                user_input = input(f"\n{YELLOW}Try again >{RESET} ").strip()
            except (EOFError, KeyboardInterrupt):
                print(f"\n{DIM}Quiz ended.{RESET}")
                break
            
            if user_input.lower() in ('quit', 'exit', 'q'):
                break
            
            normalized_input = normalize_romaji(user_input)
            
            if normalized_input == normalized_expected:
                print(f"{GREEN}✓ Correct on second try!{RESET}")
                update_quiz_stat(level, slug, True)
                correct_count += 1
            else:
                print(f"{RED}✗ Incorrect.{RESET}")
                print(f"{GREEN}Correct answer: {reading} ({expected_romaji}){RESET}")
                print(f"{BLUE}{meaning_str}{RESET}")
                update_quiz_stat(level, slug, False)
                incorrect_count += 1
            
            if pos:
                print(f"{DIM}{pos} • {level}{RESET}")
        
        print()
        
        # Ask to continue
        try:
            continue_input = input(f"{DIM}Continue? (y/n):{RESET} ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print(f"\n{DIM}Quiz ended.{RESET}")
            break
        
        if continue_input not in ('y', 'yes', ''):
            break
        
        print()
    
    # Show session stats
    print(f"\n{CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}")
    print(f"{YELLOW}Session Summary{RESET}")
    print(f"{GREEN}Correct: {correct_count}{RESET}")
    print(f"{RED}Incorrect: {incorrect_count}{RESET}")
    if correct_count + incorrect_count > 0:
        accuracy = (correct_count / (correct_count + incorrect_count)) * 100
        print(f"{BLUE}Accuracy: {accuracy:.1f}%{RESET}")
    print()


def select_quiz_word(words: list, stats: dict) -> dict:
    """Select a word for quiz, prioritizing less-practiced words."""
    if not words:
        return None
    
    # Score words (lower score = higher priority)
    scored_words = []
    for word in words:
        slug = word.get("slug", "")
        word_stats = stats.get(slug, {"correct": 0, "incorrect": 0})
        
        # Prioritize words with fewer correct answers
        score = word_stats["correct"] * 10 - word_stats["incorrect"] * 2
        scored_words.append((score, word))
    
    # Sort by score and add randomness to top candidates
    scored_words.sort(key=lambda x: x[0])
    top_candidates = scored_words[:min(10, len(scored_words))]
    
    return random.choice(top_candidates)[1] if top_candidates else random.choice(words)


def main():
    parser = argparse.ArgumentParser(
        description="JLPT vocabulary quiz tool"
    )
    parser.add_argument(
        "--level",
        choices=["N5", "N4", "N3", "N2", "N1"],
        help="Specify JLPT level (default: random)"
    )
    parser.add_argument(
        "--offline",
        action="store_true",
        help="Use cached words only (no internet required)"
    )
    
    args = parser.parse_args()
    
    os.makedirs(CACHE_DIR, exist_ok=True)
    
    # Determine level
    level = args.level if args.level else random.choice(["N5", "N4", "N3", "N2", "N1"])
    
    quiz_mode(level, args.offline)


if __name__ == "__main__":
    main()
