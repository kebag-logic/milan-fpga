#!/usr/bin/env bash
set -u
packet=$(cd -- "$(dirname -- "$0")/.." && pwd)
source_tree=${1:?usage: probe.sh SOURCE_TREE}
export TMPDIR="$packet/scratch"
export MAKEFLAGS=-j16
mkdir -p "$packet/receipts/occupancy"
$VALIDATION_TOOLS/pinned-verilator-5.050/verilator --version > "$packet/receipts/compiler-identity.txt"
sha256sum $VALIDATION_TOOLS/pinned-verilator-5.050/verilator >> "$packet/receipts/compiler-identity.txt"
python3 "$source_tree/tb/pp_top/notify_mutants.py" --output "$packet/receipts/occupancy" --verilator "$packet/scripts/capped_verilator.py" --jobs 3 --only occupancy_cleared_beside_push occupancy_not_busy occupancy_pop_clears > "$packet/receipts/occupancy-campaign.log" 2>&1
rc=$?
printf '%s\n' "$rc" > "$packet/receipts/occupancy-campaign.rc"
cat "$packet/receipts/occupancy-campaign.log"
exit "$rc"
