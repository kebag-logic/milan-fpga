#!/bin/bash
# run_suite.sh TREE SUITE CPUS OUT [make args...]
# Runs `make -C tb/verilator/SUITE [args]` in TREE pinned to CPUS with the hosted
# job budgets, writing OUT.log, OUT.rc and OUT.time (GNU time -v).
set -u
TREE=$1 SUITE=$2 CPUS=$3 OUT=$4
shift 4
HERE=$(cd "$(dirname "$0")" && pwd)
export VERILATOR="$HERE/vwrap.sh" VW_JOBS=2
export VERILATOR_JOBS=2 SIM_JOBS=2 MAKEFLAGS='-j1 --no-print-directory'
# verilator_coverage and any bare `verilator` resolve to the pinned tool through
# host-local shims in $HERE/bin (not published: bin/verilator -> vwrap.sh, and
# bin/verilator_coverage execs the pinned install's verilator_coverage)
export PATH="$HERE/bin:$PATH"
cd "$TREE" || exit 2
/usr/bin/time -v -o "$OUT.time" taskset -c "$CPUS" make -C "tb/verilator/$SUITE" "$@" > "$OUT.log" 2>&1
echo $? > "$OUT.rc"
