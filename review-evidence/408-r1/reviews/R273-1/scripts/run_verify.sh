#!/usr/bin/env bash
# Independent verification of another review's findings: base and head, SDK and absent.
# Usage: run_verify.sh <packet> <sdk> <cases.json> <tag>
set -u
packet=$1; sdk=$2; cases=$3; tag=$4; out=$packet/receipts/70-verify; mkdir -p "$out"
for side in base head; do
  for mode in sdk absent; do
    if [ "$mode" = sdk ]; then flag=(--sdk "$sdk"); else flag=(--absent); fi
    ( cd "$packet/scratch/$side" || exit 2
      python3 -B "$packet/scripts/probe.py" --checkout . "${flag[@]}" --cases "$cases" \
        --out "$out/$tag-$side-$mode.json" > "$out/$tag-$side-$mode.txt" 2>&1
      echo "exit=$?" >> "$out/$tag-$side-$mode.txt" ) &
  done
done
wait
python3 - "$out" "$tag" <<'PY'
import json, sys
from pathlib import Path
out, tag = Path(sys.argv[1]), sys.argv[2]
runs = {f"{s}-{m}": json.loads((out / f"{tag}-{s}-{m}.json").read_text())
        for s in ("base", "head") for m in ("sdk", "absent")}
labels = [r["label"] for r in runs["base-sdk"]]
print(f"{'case':<10}" + "".join(f"{k:>14}" for k in runs))
for i, label in enumerate(labels):
    print(f"{label.split()[0]:<10}" + "".join(f"{runs[k][i]['verdict']:>14}" for k in runs))
PY
