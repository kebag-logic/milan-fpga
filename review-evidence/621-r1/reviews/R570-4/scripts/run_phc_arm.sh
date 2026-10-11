#!/usr/bin/env bash
# Usage: [VERILATOR_DIR=<dir>] run_phc_arm.sh <clone root> <generator> <work dir> <log> <rc file>
# Runs the #621 step regression (tb/verilator/gptp_plane/phc_step.py, clean arm
# only) against one generator variant written by probe_phc_step_plants.py.
set -u
[ -n "${VERILATOR_DIR:-}" ] && export PATH="$VERILATOR_DIR:$PATH"
cd "$1/tb/verilator/gptp_plane" || exit 2
python3 phc_step.py --generator "$2" --work "$3" > "$4" 2>&1
echo "rc=$?" > "$5"
