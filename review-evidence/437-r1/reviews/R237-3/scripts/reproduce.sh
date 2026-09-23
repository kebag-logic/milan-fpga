#!/usr/bin/env bash
# Reproduce this round's measurements from the packet root.
# Usage: scripts/reproduce.sh <clone-at-any-commit-containing-the-three-revisions>
# Renders are cached under receipts/renders; with the cache present no
# page is sent to GitHub again. Needs python3 and an authenticated gh.
set -euo pipefail
clone=$1
base=574c29fa111c74e5e5ed63e4670aff1f492e28e2
head=e4906bfca65c61e7e109e3532ac1b2dd5b4c0096
mkdir -p scratch/base scratch/head
git -C "$clone" archive "$base" scripts | tar -x -C scratch/base
git -C "$clone" archive "$head" scripts | tar -x -C scratch/head
B=scratch/base/scripts H=scratch/head/scripts
python3 -B scripts/rerender_fixtures.py "$H" "$B" receipts/fixture_renders receipts/fixture_rerender.json
python3 -B scripts/compare.py receipts/pages/minimal.json receipts/minimal head="$H" base="$B"
python3 -B scripts/compare.py receipts/pages/fuzz_full_sample.json receipts/fuzz1 head="$H" base="$B"
python3 -B scripts/per_heading.py receipts/fuzz1.json receipts/pages/fuzz_full_sample.json receipts/fuzz1.per_heading.txt
python3 -B scripts/compare.py receipts/pages/fuzz_core_sample.json receipts/fuzz_core head="$H" base="$B"
python3 -B scripts/per_heading.py receipts/fuzz_core.json receipts/pages/fuzz_core_sample.json receipts/fuzz_core.per_heading.txt
python3 -B scripts/emdash_e2e.py "$B" base; python3 -B scripts/emdash_e2e.py "$H" head
python3 -B scripts/mutate.py "$H" scratch receipts/mutations.txt
for rev in "$head" "$base"; do
  python3 -B scripts/ac4_classification.py "$clone" "$rev" "$B" "$H" "receipts/ac4_${rev:0:12}.json"
done
# The page sets were drawn with scripts/gen_pages.py (seed 437 full, seed
# 4371 `core`, 30000 pages each) and sampled; the samples are in receipts/pages.
