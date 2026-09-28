#!/usr/bin/env bash
# Usage: apply_check.sh <processor-clone> <scratch-dir>
# git apply --check of every committed patch against a fresh copy of the head's hdl/,
# outside any repository (as mutants.py does), then a clean apply and reverse check.
set -u
pp=$(cd "$1" && pwd); s=$2; n=0; bad=0
for p in "$pp"/tb/srp_top/mutations/*.patch; do
  t=$s/apply-check; rm -rf "$t"; mkdir -p "$t"; git -C "$pp" archive 0404675dcd8788d29cb15a831a8c182438bf1c92 hdl | tar -x -C "$t"
  (cd "$t" && git apply --check "$p" && git apply "$p" && git apply -R --check "$p"); rc=$?
  n=$((n+1)); [ $rc -eq 0 ] || bad=$((bad+1)); echo "$(basename "$p") rc=$rc"
done
rm -rf "$s/apply-check"; echo "patches=$n failed=$bad"
