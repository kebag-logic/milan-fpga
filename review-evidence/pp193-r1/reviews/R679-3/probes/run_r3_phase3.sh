#!/bin/sh
# Round-3 reviewer probes, phase 3: does the srp_top suite (every group,
# through the real encoder and slot pool) see rv3-done-before-rewalk?
# usage: run_r3_phase3.sh <clone> <head> <outdir>
# Needs Verilator 5.050 as `verilator` on PATH.
#   top-head  head, tb/srp_top `make`
#   top-mut   head with make_r3_mutants.py rv3-done-before-rewalk, tb/srp_top `make`
set -u
clone=$1; head=$2; out=$3
here=$(cd "$(dirname "$0")" && pwd)
mkdir -p "$out"
export_to() { rm -rf "$2"; mkdir -p "$2"; git -C "$clone" archive "$1" | tar -x -C "$2"; }
export_to "$head" "$out/top-head"
export_to "$head" "$out/top-mut"; python3 -I "$here/make_r3_mutants.py" "$out/top-mut" rv3-done-before-rewalk
for n in top-head top-mut; do
  ( cd "$out/$n/tb/srp_top" && timeout 2400 make > "$out/$n.log" 2>&1; echo $? > "$out/$n.rc" ) &
done
wait
for n in top-head top-mut; do
  printf '%-9s rc=%s  %s\n' "$n" "$(cat "$out/$n.rc")" "$(grep -E '^[0-9]+ checks:' "$out/$n.log" | tail -1)"
  grep -E '^FAIL' "$out/$n.log" | cut -c1-200 | head -10
done
