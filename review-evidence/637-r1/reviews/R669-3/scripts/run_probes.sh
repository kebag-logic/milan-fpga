#!/bin/sh
# Rerun dynmap_mutants rows 61-63 and reviewer probe L against the clone.
# Usage: run_probes.sh <clone> <pinned-verilator-dir> <receipt-dir> <tmpdir>
set -u
C=$1; VD=$2; R=$3; T=$4
mkdir -p "$T"
cd "$C/tb/verilator/milan_dp" || exit 9
TMPDIR=$T PATH=$VD:$PATH VERILATOR=$VD/verilator VERILATOR_JOBS=4 \
  python3 -I "$(dirname "$0")/probe_mutants.py" "$C" 4 61 62 63 L > "$R/probes.log" 2>&1
echo $? > "$R/probes.rc"
