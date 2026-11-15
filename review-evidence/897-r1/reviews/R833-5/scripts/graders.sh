#!/usr/bin/env bash
# Run the portable graders and self-tests of the CPU service budget harness concurrently.
# usage: graders.sh CLONE OUTDIR SCRATCH
set -u
clone=$1; out=$2; scratch=$3
mkdir -p "$out" "$scratch"
cd "$clone/tb/verilator/ctrl_service_budget" || exit 2
run() { local name=$1; shift; ( "$@" > "$out/$name.log" 2>&1; echo $? > "$out/$name.rc" ) & }
run harness-selftest python3 -B run.py --self-test
run flip-1x1 python3 -I flip_grade.py --check --point 1x1/1if
run load-check python3 -I load_grade.py --check
run load-selftest python3 -I load_grade.py --selftest
run tier_grid-1x1 python3 -I tier_grid.py --point 1x1/1if --out "$scratch/tg"
run flip-selftest python3 -I flip_grade.py --selftest
wait
for f in "$out"/*.rc; do echo "$(basename "$f") $(cat "$f")"; done
