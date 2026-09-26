#!/usr/bin/env bash
# Run after the verdict and ledger were written: fetch the reviews/ part of the public
# evidence tree (milan-fpga 356583ef) and verify its MANIFEST.json hashes. Read-only.
set -uo pipefail
PK=$(cd "$(dirname "$0")/.." && pwd); D=$PK/scratch/evidence; cd $D
[ -f list.txt ] || { echo "run 09-public-evidence.sh first"; exit 2; }
grep '/reviews/' list.txt > list-reviews.txt
while read -r sha p; do [ -f "$p" ] || { mkdir -p "$(dirname "$p")"; gh api -H 'Accept: application/vnd.github.raw' "repos/kebag-logic/milan-fpga/git/blobs/$sha" > "$p"; }; done < list-reviews.txt
cd review-evidence/pp120-r1
python3 - <<'P'
import json, hashlib, collections
m = json.load(open("MANIFEST.json"))
bad = [e["file"] for e in m if hashlib.sha256(open(e["file"], "rb").read()).hexdigest() != e["published_sha256"]]
print(f"MANIFEST.json: {len(m)} entries (all), {len(bad)} hash mismatches {bad[:3]}")
print("reviews/ packets:", dict(collections.Counter("/".join(e["file"].split("/")[:2]) for e in m if e["file"].startswith("reviews/"))))
P
