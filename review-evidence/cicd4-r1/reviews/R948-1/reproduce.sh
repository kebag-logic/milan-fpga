#!/usr/bin/env bash
# Reproduce focused review checks from the isolated candidate checkout.
set -euo pipefail
review_root="$(git rev-parse --show-toplevel)"
review_packet="$(cd -- "$(dirname -- "$0")" && pwd)"
mkdir -p "$review_packet/scratch"
export TMPDIR="$review_packet/scratch" PYTHONDONTWRITEBYTECODE=1
# The published evidence commit must be fetched read-only first if absent.
git cat-file -e 6be24f180ccc2c0ddda4b5d3ffa40ba09d7885e3^{commit}
git archive 6be24f180ccc2c0ddda4b5d3ffa40ba09d7885e3 \
  review-evidence/cicd4-r1/author/receipts review-evidence/cicd4-r1/MANIFEST.json \
  review-evidence/cicd4-r1/author/REVIEW-READY.md | tar -x -C "$review_packet/scratch"
python3 "$review_packet/run_checks.py" "$review_root"
python3 "$review_packet/probe_receipts.py" "$review_root"
python3 "$review_packet/audit_schedule.py" "$review_root"
python3 "$review_packet/inspect_evidence.py" "$review_root" "$review_packet/scratch/review-evidence/cicd4-r1"
review_receipts="$review_packet/scratch/review-evidence/cicd4-r1/author/receipts"
python3 "$review_receipts/tools/project.py"
python3 "$review_receipts/tools/minutes.py"
python3 "$review_root/scripts/suite_shards.py" --measure \
  "$review_receipts/hosted/45657606190-w22-raw.log" \
  "$review_receipts/hosted/45751066654-w22-raw.log"
python3 "$review_packet/verify_tree.py" "$review_root"
