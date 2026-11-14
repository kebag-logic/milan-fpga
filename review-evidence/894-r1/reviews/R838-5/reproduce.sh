#!/bin/sh
# Run from anywhere; supply the exact-head checkout and this packet directory.
set -eu
repo=$(realpath "$1")
packet=$(realpath "$2")
mkdir -p "$packet/scratch"
git -C "$repo" archive 56e8f05bc2fa6d733d6b5c637bf1501d19dbe8dc \
  review-evidence/894-r1/MANIFEST.json review-evidence/894-r1/author-r10 review-evidence/894-r1/author-r9 \
  > "$packet/scratch/public-evidence.tar"
tar -xf "$packet/scratch/public-evidence.tar" -C "$packet/scratch"
python3 -B "$packet/probe.py" "$repo" "$packet"
python3 -B "$packet/weak_assertion.py" "$repo" "$packet"
python3 -B "$packet/audit_docs.py" "$repo" "$packet"
python3 -B "$packet/verify_checkout.py" "$repo" "$packet"
