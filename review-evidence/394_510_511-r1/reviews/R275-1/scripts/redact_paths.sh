#!/usr/bin/env bash
# Replace host-specific absolute paths in published receipts with neutral
# placeholders, in place. Usage: redact_paths.sh <packet> <clone> <tool-bin> <home>
set -u
packet=$1; clone=$2; tools=$3; home=$4
find "$packet/receipts" -type f -print0 | while IFS= read -r -d '' f; do
  sed -i -e "s#${packet}#\$PACKET#g" -e "s#${clone}#\$CLONE#g" \
         -e "s#${tools}#\$PINNED_TOOL_BIN#g" -e "s#${home}#\$HOME#g" "$f"
done
