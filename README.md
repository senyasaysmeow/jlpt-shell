# JLPT Shell Greeting

A terminal greeting script that displays a random Japanese vocabulary word from the JLPT (Japanese Language Proficiency Test) every time you open a new terminal session.

## Features

- 🎲 **Random JLPT words** from all levels (N5-N1)
- 📚 **Automatic level selection** - randomly picks a JLPT level each session
- 🔄 **Smart tracking** - remembers which words you've seen and shows new ones
- 🌐 **Real-time data** - fetches words from [Jisho.org](https://jisho.org) API
- 🎨 **Colorful output** - beautifully formatted with kanji, reading, and meanings
- ⚡ **Fast and lightweight** - minimal dependencies

## Preview

```
📚 JLPT Word of the Session
食べる  (たべる)
to eat, to live on (e.g. a salary), to live off, to subsist on
Verb N5
```

## Installation

### Prerequisites

- Python 3.x
- Zsh (for shell integration)

### Setup

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/jlpt-shell.git
   cd jlpt-shell
   ```

2. Make the scripts executable:
   ```bash
   chmod +x jlpt_greeting.py
   chmod +x jlpt-greeting.zsh
   ```

3. Add to your `.zshrc` to run on every terminal session:
   ```bash
   echo 'source /path/to/jlpt-shell/jlpt-greeting.zsh' >> ~/.zshrc
   ```
   
   Replace `/path/to/jlpt-shell` with the actual path to this repository.

4. Reload your shell:
   ```bash
   source ~/.zshrc
   ```

## Usage

### Automatic (Recommended)

Once installed in your `.zshrc`, a new JLPT word will appear every time you open a new terminal session.

### Manual

You can also run the script manually anytime:

```bash
python3 jlpt_greeting.py
```

Or using the Zsh wrapper:

```bash
./jlpt-greeting.zsh
```

## How It Works

1. The script randomly selects a JLPT level (N5, N4, N3, N2, or N1)
2. Fetches vocabulary data from the Jisho.org API
3. Tracks previously shown words in `~/.cache/jlpt-greeting/`
4. Displays a new word with:
   - Kanji (if available)
   - Reading (hiragana/katakana)
   - English meanings
   - Part of speech and JLPT level
5. When all words from a level have been shown, the cycle resets

## Configuration

You can modify the `JLPT_LEVEL` variable in `jlpt_greeting.py` to focus on a specific level:

```python
# Random level (default)
JLPT_LEVEL = random.choice(["N5", "N4", "N3", "N2", "N1"])

# Or fix to a specific level
JLPT_LEVEL = "N3"
```

## Cache Management

The script caches which words you've seen in:
```
~/.cache/jlpt-greeting/shown_N*.txt
```

To reset and see all words again, simply delete these files:
```bash
rm -rf ~/.cache/jlpt-greeting/
```

## JLPT Levels

- **N5** - Basic level (beginner)
- **N4** - Elementary level
- **N3** - Intermediate level
- **N2** - Advanced level
- **N1** - Expert level (most difficult)

## Dependencies

- Python 3.x standard library only (no external packages required!)
- Internet connection (for fetching words from Jisho.org)

## Troubleshooting

### Script doesn't run on terminal open
- Verify the path in your `.zshrc` is correct
- Check that scripts are executable: `ls -l jlpt_greeting.py`
- Try running manually to see error messages

### No words displayed
- Check your internet connection
- The Jisho.org API might be temporarily unavailable
- Try running manually to see specific error messages

### "No vocabulary found" message
- This is rare but can happen if the API returns no results
- Simply open a new terminal session to try again

## Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests

## License

MIT License - feel free to use and modify as you wish.

## Credits

- Vocabulary data powered by [Jisho.org](https://jisho.org)
- Inspired by the need to practice Japanese vocabulary daily

## Acknowledgments

Special thanks to the Jisho.org team for providing a free and reliable Japanese dictionary API.

---

**Happy learning! 頑張って！(がんばって / Ganbatte / Good luck!)**
