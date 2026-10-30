#!/usr/bin/env bash
# Run the gate's self-test, check-baseline and its mutant campaign (16 workers) concurrently at the reviewed clone.
# usage: run_gate_suites.sh <clone> <out>
set -u
C=$1 O=$2; mkdir -p "$O"
G=$C/syn/ooc
( python3 -B "$G/pp_resource_gate.py" --selftest > "$O/selftest.log" 2>&1; echo $? > "$O/selftest.rc" ) &
( python3 -B "$G/pp_resource_gate.py" check-baseline > "$O/check-baseline.log" 2>&1; echo $? > "$O/check-baseline.rc" ) &
( python3 -B -c 'import os,runpy,sys; os.cpu_count=lambda: 16; sys.argv=[sys.argv[1]]; sys.path.insert(0, os.path.dirname(sys.argv[0])); runpy.run_path(sys.argv[0], run_name="__main__")' "$G/pp_resource_gate_mutants.py" > "$O/mutants.log" 2>&1; echo $? > "$O/mutants.rc" ) &
wait
for f in "$O"/*.rc; do echo "$(basename "$f" .rc) rc=$(cat "$f")"; done
