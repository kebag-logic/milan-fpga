#!/bin/sh
# Round R754-5 probes at head ef7dc985. Usage: run_probes.sh <head-clone> <packet-dir>
# Runs concurrently: generator --check and --selftest, the read sweep at head,
# the sweep against the page with the replaced wording planted back
# (79fdea05's page), and the sweep over two RTL mutants of the srp_fresh_r
# clears (m1: stolen clear removed; m2: a write answer sets instead of clears).
set -u
C=$1; P=$2; S=$P/scratch; R=$P/receipts
mkdir -p "$R" "$S/w"
export PATH=$VALIDATION_TOOLS/pinned-verilator-5.050:$PATH
verilator --version > "$R/verilator_version.txt" 2>&1
run() { n=$1; shift; ( "$@" > "$R/$n.log" 2>&1; echo $? > "$R/$n.rc" ) & }
run gen_check    python3 -I "$C/scripts/gen_register_reference.py" --check
run gen_selftest python3 -I "$C/scripts/gen_register_reference.py" --selftest
run sweep_head   python3 -I "$C/scripts/register_read_sweep.py" --work "$S/w/head"
run sweep_oldpage python3 -I "$C/scripts/register_read_sweep.py" --page "$S/page_old_wording.md" --work "$S/w/old"
run sweep_m1     python3 -I "$S/m1/scripts/register_read_sweep.py" --work "$S/w/m1"
run sweep_m2     python3 -I "$S/m2/scripts/register_read_sweep.py" --work "$S/w/m2"
wait
for f in "$R"/*.rc; do echo "$(basename "$f" .rc) rc=$(cat "$f")"; done
