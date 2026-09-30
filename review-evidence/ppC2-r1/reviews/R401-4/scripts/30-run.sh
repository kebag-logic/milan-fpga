#!/usr/bin/env bash
# Run one target in the exported tree under the pinned Verilator, capped at 8 CPUs.
# Usage: 30-run.sh <scratch-dir> <receipt-dir> <label> <cmd...>   (cwd = tree root)
set -uo pipefail
S=${1:?}; O=${2:?}; L=${3:?}; shift 3
export PATH="$S/bin:$PATH" TMPDIR="$S/tmp"
cd "$S/tree"
date -u +%FT%TZ >"$O/$L.start"
taskset -c 0-7 "$@" >"$O/$L.log" 2>&1; rc=$?
date -u +%FT%TZ >"$O/$L.end"; echo $rc >"$O/$L.rc"
echo "$L rc=$rc $(grep -Eo '[0-9]+ checks: [0-9]+ PASS, [0-9]+ FAIL|\] [0-9]+ checks, [0-9]+ failures' "$O/$L.log" | tail -1)"
exit $rc
