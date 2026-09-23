#!/usr/bin/env bash
# Audit the head gate's own mutation table with replacements disconnected.
# Usage: run_disconnects.sh <packet-dir> <sdk-dir>
set -u
packet=$1
sdk=$2
out=$packet/receipts/30-disconnect
mkdir -p "$out"
run() {  # name mode disconnect...
  local name=$1 mode=$2
  shift 2
  local flags=()
  if [ "$mode" = sdk ]; then flags=(--sdk "$sdk"); else flags=(--absent); fi
  for d in "$@"; do flags+=(--disconnect "$d"); done
  (
    cd "$packet/scratch/head" || exit 2
    python3 -B "$packet/scripts/probe.py" --checkout . "${flags[@]}" \
      --mutation-audit --out "$out/$name.json" > "$out/$name.txt" 2>&1
    echo "exit=$?" >> "$out/$name.txt"
  ) &
}
run connected-sdk sdk
run sel-sdk sdk sel
run sel-absent absent sel
run ERC-sdk sdk E R C
run E-sdk sdk E
run H-sdk sdk H
run RC-sdk sdk R C
wait
python3 - "$out" <<'EOF'
import json, sys
from pathlib import Path
out = Path(sys.argv[1])
for f in sorted(out.glob("*.json")):
    rows = json.loads(f.read_text())
    acc = [r["label"] for r in rows if r["verdict"] == "ACCEPTED"]
    miss = [r["label"] for r in rows if r["verdict"] == "REFUSED" and not r["pin_ok"]]
    print(f"== {f.stem}: {len(rows)} entries, {len(acc)} ACCEPTED, "
          f"{len(miss)} refused but PIN MISSED")
EOF
