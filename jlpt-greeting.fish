set SCRIPT_DIR (dirname (status --current-filename))

function jlpt
    python3 "$SCRIPT_DIR/jlpt_greeting.py" $argv
end
