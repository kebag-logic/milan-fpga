#!/bin/sh
# Run the named mutants, JOBS (default 8, at most 8) at a time, each into
# receipts/mut/<M>.log, each bounded by TMO seconds (default 570).
# Usage: run_batch.sh <runner: run_mutant.sh|run_mutant_extra.sh> M...
set -u
. "$(dirname "$0")/env.sh"
R="$1"; shift
: "${JOBS:=8}"; : "${TMO:=570}"
[ "$JOBS" -le 8 ] || JOBS=8
mkdir -p "$PKT/receipts/mut"
printf '%s\n' "$@" | xargs -P "$JOBS" -I{} sh -c "timeout $TMO \"$PKT/scripts/$R\" {} > \"$PKT/receipts/mut/{}.log\" 2>&1; echo \"{} rc=\$?\""
