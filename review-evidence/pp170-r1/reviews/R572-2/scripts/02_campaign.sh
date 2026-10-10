#!/bin/sh
# Full name mutation campaign at the exact head. Usage: 02_campaign.sh [jobs]
set -u; . "$(dirname "$0")/env.sh"
t="$SCRATCH/campaign"; extract "$t/src"; rm -rf "$t/out"
python3 "$t/src/tb/name_state/mutants.py" --root "$t/src" --verilator "$VERILATOR" --jobs "${1:-6}" --output "$t/out" > "$RCPT/campaign.log" 2>&1
echo $? > "$RCPT/campaign.rc"
cp "$t/out/results.json" "$RCPT/campaign-results.json" 2>/dev/null
for f in "$t"/out/*/names-*/run.log; do c=${f#$t/out/}; c=$(echo "$c" | tr / _); cp "$f" "$RCPT/campaign-$c"; done
