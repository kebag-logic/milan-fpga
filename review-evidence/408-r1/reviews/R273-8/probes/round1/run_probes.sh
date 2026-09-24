#!/usr/bin/env bash
# Grade the reviewer's cases at base and head, with the pinned SDK and with
# every cross compiler hidden: four parallel probe.py runs.
# Usage: run_probes.sh <packet-dir> <sdk-dir>
set -u
packet=$1
sdk=$2
cases=$packet/cases
out=$packet/receipts/20-probes
mkdir -p "$out"
python3 - "$cases" <<'EOF'
import json, sys
from pathlib import Path
c = Path(sys.argv[1])
acc, hos = (json.loads((c / f"{n}.json").read_text()) for n in ("accepted", "hostile"))
for side in ("base", "head"):
    lst = json.loads((c / f"listing_{side}.json").read_text())
    (c / f"all_{side}.json").write_text(json.dumps(acc + hos + lst, indent=1) + "\n")
EOF
for side in base head; do
  for mode in sdk absent; do
    if [ "$mode" = sdk ]; then flag=(--sdk "$sdk"); else flag=(--absent); fi
    (
      cd "$packet/scratch/$side" || exit 2
      python3 -B "$packet/scripts/probe.py" --checkout . "${flag[@]}" \
        --cases "$cases/all_$side.json" --out "$out/$side-$mode.json" \
        > "$out/$side-$mode.txt" 2>&1
      echo "exit=$?" >> "$out/$side-$mode.txt"
    ) &
  done
done
wait
for f in "$out"/*.txt; do echo "=== $f"; grep -E '^(ACCEPTED|REFUSED)|^mode=|^exit=' "$f"; done
