# JLPT Quiz

An interactive terminal quiz tool for practicing JLPT (Japanese Language Proficiency Test) vocabulary. Get tested on kanji, get hints when you're stuck, and practice offline with cached words.

## Features

- 🎯 **Kanji-first learning** - See only the kanji, no hints unless you need them
- 💡 **Smart hints** - Get the English meaning if you answer incorrectly on first try
- 🔄 **Second chance** - Try again after seeing the hint
- 💾 **Offline practice** - Words are cached locally for learning without internet
- 📊 **Progress tracking** - Tracks your correct/incorrect answers
- 🎲 **Spaced repetition** - Prioritizes words you struggle with
- ⚡ **No dependencies** - Uses only Python 3 standard library

## Installation

### Prerequisites

- Python 3.x
- Terminal (zsh recommended for shell integration)

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/jlpt-shell.git
   cd jlpt-shell
   ```

2. Make scripts executable:
   ```bash
   chmod +x jlpt_greeting.py
   chmod +x jlpt-greeting.zsh
   ```

3. (Optional) Add to `.zshrc` for easy access:
   ```bash
   source /path/to/jlpt-shell/jlpt-greeting.zsh
   ```

## Usage

### Quick Start

```bash
# Start quiz with random JLPT level
python3 jlpt_greeting.py

# Or using the alias (if sourced in .zshrc)
jlpt-quiz
```

### Command Options

```bash
# Quiz specific JLPT level (N5-N1)
python3 jlpt_greeting.py --level N3

# Practice offline (no internet required)
python3 jlpt_greeting.py --offline

# Combine options
python3 jlpt_greeting.py --level N5 --offline
```

### Full Help

```bash
python3 jlpt_greeting.py --help
```

## How It Works

### Quiz Flow

1. **Kanji Only** - You see only the kanji/word
   ```
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   食べる
   Romaji >
   ```

2. **First Attempt** - Type the romaji reading
   - ✓ **Correct?** → Shows meaning and moves to next word
   - ✗ **Wrong?** → Shows meaning as a hint, gives you a second try

3. **Second Attempt** (if needed) - Try again with the hint
   - ✓ **Correct?** → Counts as correct, moves to next word
   - ✗ **Wrong?** → Shows correct answer, marks as incorrect

### Example Session

```
🎯 JLPT Quiz Mode - N5
Type the romaji reading for each kanji. Type 'quit' to exit.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
食べる

Romaji > taberu
✓ Correct!
to eat, to live on (e.g. a salary)
Ichidan verb • N5

Continue? (y/n): y

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
学校

Romaji > gakkou
✗ Incorrect.
Hint - Meaning: school, School

Try again > gakkō
✓ Correct on second try!
Ichidan verb • N5

Continue? (y/n):
```

## JLPT Levels

- **N5** - Beginner level
- **N4** - Elementary level
- **N3** - Intermediate level
- **N2** - Advanced level
- **N1** - Proficiency level (most difficult)

## Cache & Data

### Cache Location

Words and statistics are stored in:
```
~/.cache/jlpt-quiz/
```

Files:
- `words_N*.json` - Cached vocabulary for each level
- `quiz_stats_N*.json` - Your performance stats (correct/incorrect counts)

### Building Your Cache

Words are automatically cached as you quiz:
1. First time online - Words are fetched from Jisho.org API and cached
2. After that - Use `--offline` to practice without internet
3. Cache grows as you use the tool - More words = more practice material

### Reset Cache

To reset and start fresh:
```bash
# Delete everything
rm -rf ~/.cache/jlpt-quiz/

# Keep words but reset stats
rm ~/.cache/jlpt-quiz/quiz_stats_*.json
```

## Learning Tips

1. **Start with N5** - Build fundamentals before moving up
2. **Practice regularly** - Small daily sessions are more effective
3. **Use offline mode** - Practice anywhere without internet
4. **Focus on weak words** - The tool prioritizes words you struggle with
5. **Second attempt learning** - The hint helps cement the connection

## Commands During Quiz

- Type **romaji** to answer
- Type **quit**, **exit**, or **q** to stop the quiz
- Press **Enter** on "Continue?" to keep going (defaults to yes)

## Troubleshooting

### "No cached words available"
- Run online mode first: `python3 jlpt_greeting.py --level N5`
- This downloads and caches words from Jisho.org

### Answer marked wrong but seems right
- Romaji uses flexible matching for common variations (ou/ō, uu/ū)
- The quiz expects the specific reading from the API
- Some kanji have multiple readings; the quiz tests one specific reading

### No internet connection
- Use `--offline` flag to practice with cached words
- Build cache during online sessions for offline use

## Data Source

Words and readings are fetched from [Jisho.org](https://jisho.org) - a free Japanese dictionary API.

## Requirements

- Python 3.x (standard library only - no pip packages needed)
- Internet connection (for initial word fetching; cached mode requires no internet)

## License

MIT

## Contributing

Feel free to:
- Report bugs
- Suggest features
- Improve the tool

## Future Ideas

- Stats dashboard showing progress over time
- Difficulty levels within each JLPT level
- Custom word lists
- Audio pronunciation
- Kanji stroke order visualization
