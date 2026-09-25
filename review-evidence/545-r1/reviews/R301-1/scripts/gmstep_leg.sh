#!/usr/bin/env bash
# Build and run the connected milan_dp gmstep leg (includes the #545 slew
# phase) at the head, objects in scratch; then the two #545 connection
# controls via gmstep_mutants.py --slew (one datapath elaboration each).
set -u
REPO=${REPO:-$REVIEWS/r301-1-545}
PKT=${PKT:-$REVIEWS/545-r301-1-packet}
export VERILATOR=${VERILATOR:-$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin/verilator}
export PATH="$(dirname "$VERILATOR"):$PATH"
MODE=${1:-leg}
cd "$REPO/tb/verilator/milan_dp" || exit 2
if [ "$MODE" = leg ]; then
  make gmstep GMSTEP_MDIR="$(realpath --relative-to=. "$PKT/scratch/obj_gmstep")" VERILATOR="$VERILATOR"
else
  python3 gmstep_mutants.py --slew
fi
