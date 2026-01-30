#!/bin/bash
# OpenSH - Unix Uninstaller
# Based on nlsh (https://github.com/junaid-mahmood/nlsh)

echo "Uninstalling OpenSH..."

rm -rf "$HOME/.opsh"
rm -f "$HOME/.local/bin/opsh"

# Remove auto-start lines from shell configs
for rc_file in "$HOME/.zprofile" "$HOME/.zshrc" "$HOME/.bashrc" "$HOME/.bash_profile"; do
    if [ -f "$rc_file" ]; then
        # Remove OpenSH auto-start line (if exists)
        sed -i '' '/opsh # auto-start/d' "$rc_file" 2>/dev/null || sed -i '/opsh # auto-start/d' "$rc_file" 2>/dev/null
        sed -i '' '/OpenSH - auto-start/d' "$rc_file" 2>/dev/null || sed -i '/OpenSH - auto-start/d' "$rc_file" 2>/dev/null
    fi
done

echo "✓ OpenSH has been removed"
