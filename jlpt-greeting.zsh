#!/bin/zsh

# JLPT Terminal Greeting Script
# Simply runs the Python script that does all the work

SCRIPT_DIR="${0:A:h}"
python3 "$SCRIPT_DIR/jlpt_greeting.py"
