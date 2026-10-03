#!/usr/bin/env bash
# Compare this round's probe receipts with round 3's, case by case: rc, and the
# verdict lines (lines starting "YOSYS" or naming the census), byte for byte.
# usage: compare_vs_r3.sh <r3-dir> <r4-dir>
set -uo pipefail
a=$1 b=$2
v() { grep -E '^(YOSYS|modules declared|tops array|yosys parsed)' "$1" | sed -E 's#/[^ ]*/(probe|census)-[^/ ]*/#<tree>/#g'; }
for f in "$b"/*.rc; do
  c=$(basename "$f" .rc)
  [ -f "$a/$c.rc" ] || { echo "$c: no r3 receipt"; continue; }
  if diff <(v "$a/$c.log") <(v "$b/$c.log") >/dev/null; then s=SAME; else s=DIFF; fi
  echo "$c rc r3=$(cat "$a/$c.rc") r4=$(cat "$f") verdict-lines $s"
done
