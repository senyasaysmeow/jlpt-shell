#!/bin/zsh

# JLPT Quiz Script
# Launches the JLPT vocabulary quiz

SCRIPT_DIR="${0:A:h}"

# Create function for quiz
jlpt-quiz() {
    python3 "$SCRIPT_DIR/jlpt_greeting.py" "$@"
}

# Alias for convenience
alias jlpt='python3 "'$SCRIPT_DIR'/jlpt_greeting.py"'
