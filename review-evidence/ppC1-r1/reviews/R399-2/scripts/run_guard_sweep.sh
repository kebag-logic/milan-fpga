#!/usr/bin/env bash
# R399-2: run probe_guard.py over a job list, at most 8 in parallel.
# Args: <pristine tree at 412efeb7> <work dir> <jobs file: name now0 arm mutant(-=none) drop>
set -euo pipefail
TREE=$1; WORK=$2; JOBS=$3; HERE=$(cd "$(dirname "$0")" && pwd)
mkdir -p "$WORK"
run_one() { # name now0 arm mut drop
  local mut=$4; [ "$mut" = "-" ] && mut=""
  NOW0=$2 ARM=$3 MUT=$mut DROP=$5 python3 "$HERE/probe_guard.py" "$TREE" "$WORK" "$1" >/dev/null 2>&1 || true
  echo "$1 $(grep -E 'checks:' "$WORK/$1.log" || echo NO-TALLY)"
}
export -f run_one; export TREE WORK HERE
grep -v '^#' "$JOBS" | xargs -P8 -L1 bash -c 'run_one "$@"' _
