#!/usr/bin/env bash
# Re-run the findings page's three reproduction steps (Artifact hashes, steps 1-3)
# on review-evidence/b5-r1/{author,author-r2,author-r3} at the pinned archive
# commit, from those three directories alone, and compare byte for byte.
# usage: repro_pinned.sh <git-repo-holding-the-commit> <work-dir>
set -euo pipefail
repo=$1 work=$2
pin=8e6be4329008137a152f9171638e48a43e549fb7
want=2183d57f0646cf94405b95aea5547b83f5ff0b9190ac0bd1bdcc87760c919961
rm -rf "$work"; mkdir -p "$work"
git -C "$repo" archive "$pin" review-evidence/b5-r1/author review-evidence/b5-r1/author-r2 \
  review-evidence/b5-r1/author-r3 | tar -x -C "$work"
b=$work/review-evidence/b5-r1
echo "pinned commit: $pin"
echo "masked copy before step 1: $(sha256sum < "$b/author-r2/receipts/a-long-reads.u16" | cut -d' ' -f1)"
# step 1
(cd "$b/author-r2/receipts" && gunzip -kf a-long-reads.u16.gz)
got=$(sha256sum < "$b/author-r2/receipts/a-long-reads.u16" | cut -d' ' -f1)
echo "step 1 restored read record: $got"
[ "$got" = "$want" ] && echo "step 1: MATCH page hash" || { echo "step 1: MISMATCH"; exit 1; }
# step 2
python3 -I "$b/author-r2/tools/b5_attrib.py" figures "$b/author" "$b/author-r2/receipts" > "$work/attribution.out"
if cmp -s "$work/attribution.out" "$b/author-r2/receipts/attribution.txt"; then echo "step 2: attribution.txt byte-identical ($(sha256sum < "$work/attribution.out" | cut -d' ' -f1))"; else echo "step 2: DIFFERS"; diff "$work/attribution.out" "$b/author-r2/receipts/attribution.txt" | head; exit 1; fi
# step 3
python3 -I "$b/author-r3/tools/b5_round3.py" figures "$b/author" "$b/author-r2/receipts" > "$work/round3.out"
if cmp -s "$work/round3.out" "$b/author-r3/receipts/round3_figures.txt"; then echo "step 3: round3_figures.txt byte-identical ($(sha256sum < "$work/round3.out" | cut -d' ' -f1))"; else echo "step 3: DIFFERS"; diff "$work/round3.out" "$b/author-r3/receipts/round3_figures.txt" | head; exit 1; fi
# the inputs the tools read, and whether the manifest marks them masked
python3 - "$b" <<'PY'
import json, sys, hashlib
from pathlib import Path
b = Path(sys.argv[1])
m = json.load(open(b / "author/MANIFEST.json")) if (b / "author/MANIFEST.json").exists() else None
for rel in ["summary/a-long/summary.json", "runs/a-long/events.jsonl",
            "summary/a-long/continuity-events.csv", "restore/peer-descs-2.jsonl"]:
    p = b / "author" / rel
    print("input", rel, hashlib.sha256(p.read_bytes()).hexdigest())
PY
echo "REPRO OK"
