#!/usr/bin/env bash
# Plant each reviewer probe patch into a fresh git-archive copy of the exact
# head and run tb/maap. Usage: run_probes.sh <processor checkout> <patch dir> <log dir>
# Needs env.sh sourced first (Verilator 5.050, build -j capped at 8).
set -uo pipefail
SRC=$1; PATCHES=$2; LOGS=$3
HEAD=921fff59d6e1243284e477f7a368173018420d35
mkdir -p "$LOGS"
for p in "$PATCHES"/*.patch; do
  name=$(basename "$p" .patch)
  tree=$(mktemp -d)
  git -C "$SRC" archive "$HEAD" | tar -x -C "$tree"
  if ! (cd "$tree" && git apply --check "$p" && git apply "$p"); then
    echo "$name: patch refused"; rm -rf "$tree"; continue
  fi
  make -C "$tree/tb/maap" run > "$LOGS/$name-maap.log" 2>&1
  rc=$?
  echo "$name: rc=$rc $(grep -E '^[0-9]+ checks:' "$LOGS/$name-maap.log" | tail -1)"
  grep -E '^FAIL' "$LOGS/$name-maap.log" | sed 's/^/    /'
  rm -rf "$tree"
done
