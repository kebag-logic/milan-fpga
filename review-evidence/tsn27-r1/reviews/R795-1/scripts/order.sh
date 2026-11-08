#!/bin/bash
# Entity self-test with the registry as committed, and with the two wire plants moved last (expected refusal).
set -u; . "$(dirname "$0")/env.sh"
O=$RCP/order; D=$SCR/order; mkdir -p "$O"
python3 "$REPO/scripts/entity_selftest.py" --work "$D/head-work" --select golden_planted_drift > "$O/head.log" 2>&1; echo "head rc $?" > "$O/rc.txt"
tree HEAD "$D/moved"
python3 -I - "$D/moved/tests/mutations.json" <<'PY'
import json, sys
p = json.load(open(sys.argv[1])); w = [m for m in p if m['name'].startswith('wire-put-be')]
json.dump([m for m in p if m not in w] + w, open(sys.argv[1], 'w'), indent=2)
PY
python3 "$D/moved/scripts/entity_selftest.py" --work "$D/moved-work" --select golden_planted_drift > "$O/moved.log" 2>&1; echo "moved-last rc $?" >> "$O/rc.txt"
cat "$O/rc.txt"; tail -3 "$O/moved.log"
