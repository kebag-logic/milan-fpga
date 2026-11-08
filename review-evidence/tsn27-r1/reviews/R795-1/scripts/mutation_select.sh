#!/bin/bash
# The two new plants through the repository's own mutation driver at the exact head.
set -u; . "$(dirname "$0")/env.sh"
O=$RCP/mutation-select; mkdir -p "$O"
python3 "$REPO/scripts/mutation.py" --work "$SCR/mut-select" --jobs 4 --select wire-put-be > "$O/run.log" 2>&1; echo "rc $?" > "$O/rc.txt"
python3 -I -c 'import json,sys; r=json.load(open(sys.argv[1])); [print(x["name"], x["status"], x.get("rc"), sorted(x.get("failures",{}))) for x in r]' "$SCR/mut-select/results.json" > "$O/results.txt" 2>&1
cat "$O/rc.txt" "$O/results.txt"; tail -2 "$O/run.log"
