#!/usr/bin/env bash
# Usage: run_gates.sh <clone> <gates.txt> <out-dir>. Runs each gate with its own log and rc, 8 at a time.
set -u
C=$1; L=$2; O=$3; mkdir -p "$O"; cd "$C"; export PYTHONDONTWRITEBYTECODE=1 LC_ALL=C.UTF-8
one() { n=${1%%|*}; c=${1#*|}; s=$(date +%s); timeout 540 bash -c "$c" >"$O/$n.log" 2>&1; rc=$?; echo "$rc" >"$O/$n.rc"; printf '%-20s rc=%s %ss  %s\n' "$n" "$rc" "$(( $(date +%s)-s ))" "$c"; }
export -f one; export O
xargs -a "$L" -d '\n' -P 8 -I{} bash -c 'one "$1"' _ {}
