#!/bin/sh
# The repository's documented complete gate (`make` at the root), run with the
# scoped Verilator 5.050 first on PATH. Top-level make is serial; the suite
# Makefiles build with `verilator --build -j 0` (one job per core; this host
# has `nproc` cores, recorded below) and the mutation arms with -j 4.
# Usage: full_gate.sh <label>   -> receipts/<label>.log and <label>.exit
set -u
. $REVIEWS/gptp68-a188-packet/scripts/env.sh
label=${1:-full-gate}
R=$A188_PACKET/receipts
cd "$A188_LANE" || exit 2
{
  echo "# label: $label"
  echo "# start: $(date -Is)"
  echo "# host nproc: $(nproc)"
  echo "# verilator: $(command -v verilator) -> $(verilator --version)"
  echo "# python3: $(python3 --version 2>&1); make: $(make --version | head -1)"
  echo "# head: $(git rev-parse HEAD) tree-status-before:"
  git status --porcelain
  echo "# command: make"
} > "$R/$label.log"
make >> "$R/$label.log" 2>&1
rc=$?
{
  echo "# end: $(date -Is)"
  echo "# exit: $rc"
  echo "# tree-status-after:"
  git status --porcelain
} >> "$R/$label.log"
echo "$rc" > "$R/$label.exit"
exit $rc
