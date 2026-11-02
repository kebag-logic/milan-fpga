#!/bin/sh
# Generator freshness at head ef7dc985 with wavedrom==2.0.3.post3 available.
# Usage: run_gen.sh <head-clone> <packet-dir> <python-with-wavedrom>
# gen_check: page and diagrams are what the generator emits (want 0);
# gen_selftest: planted stale-page controls (want 0);
# gen_check_oldjson: the srp_fresh_r pair planted back to 79fdea05's words
# in a disposable copy (want 1).
set -u
C=$1; P=$2; PY=$3; S=$P/scratch; R=$P/receipts
mkdir -p "$R"
run() { n=$1; shift; ( "$@" > "$R/$n.log" 2>&1; echo $? > "$R/$n.rc" ) & }
run gen_check         "$PY" -I "$C/scripts/gen_register_reference.py" --check
run gen_selftest      "$PY" -I "$C/scripts/gen_register_reference.py" --selftest
run gen_check_oldjson "$PY" -I "$S/m3/scripts/gen_register_reference.py" --check
wait
for n in gen_check gen_selftest gen_check_oldjson; do echo "$n rc=$(cat "$R/$n.rc")"; done
