#!/usr/bin/env bash
# Usage: [VERILATOR_DIR=<dir holding a verilator 5.050 executable>] \
#        run_suite.sh <clone root> <suite dir name> <log> <rc file> [make args...]
# Runs `make -C tb/verilator/<suite>` (R570-4 receipt wrapper), with
# VERILATOR_DIR first on PATH when set, and records exit status and wall time.
set -u
root=$1; suite=$2; log=$3; rcf=$4; shift 4
[ -n "${VERILATOR_DIR:-}" ] && export PATH="$VERILATOR_DIR:$PATH"
start=$(date +%s.%N)
make -C "$root/tb/verilator/$suite" "$@" > "$log" 2>&1
rc=$?
end=$(date +%s.%N)
printf 'rc=%s wall_s=%s\n' "$rc" "$(echo "$end - $start" | bc)" > "$rcf"
