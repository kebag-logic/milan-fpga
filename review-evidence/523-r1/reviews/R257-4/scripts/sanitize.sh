#!/usr/bin/env bash
# Replace workstation-local absolute paths and the local account name in the
# receipt tree with neutral placeholders. No other byte is changed.
# Usage: sanitize.sh <receipt-dir> <candidate-clone> <packet> <tool-bin> <user>
set -euo pipefail
dir=$1 clone=$2 packet=$3 toolbin=$4 user=$5
home=$(getent passwd "$user" | cut -d: -f6)
grep -rlZ -e "$clone" -e "$packet" -e "$toolbin" -e "$home" -e "$user" "$dir" |
  xargs -0 -r sed -i -E \
    -e "s#${clone}#<candidate-clone>#g" \
    -e "s#${packet}#<packet>#g" \
    -e "s#${toolbin}#<scoped-tool-bin>#g" \
    -e "s#${home}/\.local/share/containers/storage/overlay/[0-9a-f]+/diff#<tool-image-root>#g" \
    -e "s#${home}#\$HOME#g" \
    -e "s#\b${user}\b#<user>#g"
echo "remaining hits:"
grep -rn -e "$clone" -e "$packet" -e "$toolbin" -e "$home" -e "\b$user\b" "$dir" || echo "  none"
