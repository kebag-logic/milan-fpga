#!/bin/sh
# Reproduce this round's runs. usage: reproduce.sh <clean clone at ba56827b with submodules> <work dir>
# Uses the pinned simulator at $VERILATOR (default below). Builds: the head leg, the head leg without
# the listener's PROBE_TX_COMMAND, then the leg's own twelve controls plus three reviewer probes in parallel.
set -eu
clone=$1; work=$2; here=$(cd "$(dirname "$0")" && pwd)
VERILATOR=${VERILATOR:-$VALIDATION_TOOLS/pinned-verilator-5.050/verilator}; export VERILATOR
mkdir -p "$work/receipts" "$work/scratch"
for n in tree nomvrp; do mkdir -p "$work/scratch/$n"; (cd "$clone" && tar -cf - .) | tar -xf - -C "$work/scratch/$n"; done
python3 -I - "$work/scratch/nomvrp/tb/verilator/milan_dp/sim_boot_sa.cpp" <<'PY'
import sys; from pathlib import Path
p = Path(sys.argv[1]); t = p.read_text(); a = "        probe_tx();\n"
assert t.count(a) == 1; p.write_text(t.replace(a, "        // reviewer probe: no PROBE_TX_COMMAND\n"))
PY
"$here/run_leg.sh" "$work/scratch/tree" "$work/receipts/bootsa_tree.log" &
"$here/run_leg.sh" "$work/scratch/nomvrp" "$work/receipts/bootsa_nomvrp.log" &
wait
VERILATOR_JOBS=3 python3 -I "$here/par_mutants.py" "$work/scratch/tree" "$work/receipts" 6 > "$work/receipts/par_mutants.log" 2>&1
# expected: tree 67/0; nomvrp 65 checks, 1 failure (MVRP frames were sent and graded); every CASE "caught"
