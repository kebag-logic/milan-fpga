#!/bin/sh
# Round-3 reviewer probes, phase 2: the done-strobe order and a campaign
# spot-check of every srp_top control round 3 added or moved.
# usage: run_r3_phase2.sh <clone> <head> <outdir>
# Needs Verilator 5.050 as `verilator` on PATH; set TMPDIR to scratch space.
#   order-head   order_probe.py at head
#   order-mut    order_probe.py with make_r3_mutants.py rv3-done-before-rewalk
#   chain-mut    chain_probe.py with rv3-done-before-rewalk
#   camp         the head's tb/srp_top/mutants.py --only <ten arms> --jobs 8
set -u
clone=$1; head=$2; out=$3
here=$(cd "$(dirname "$0")" && pwd)
mkdir -p "$out"
export_to() { rm -rf "$2"; mkdir -p "$2"; git -C "$clone" archive "$1" | tar -x -C "$2"; }
suite() { ( cd "$out/$1/tb/srp_stream_fsms" && timeout 1500 make RUN_ARGS=suite > "$out/$1.log" 2>&1; echo $? > "$out/$1.rc" ); }

export_to "$head" "$out/order-head"; python3 -I "$here/order_probe.py" "$out/order-head/tb/srp_stream_fsms/sim_main.cpp"
export_to "$head" "$out/order-mut";  python3 -I "$here/order_probe.py" "$out/order-mut/tb/srp_stream_fsms/sim_main.cpp"
python3 -I "$here/make_r3_mutants.py" "$out/order-mut" rv3-done-before-rewalk
export_to "$head" "$out/chain-mut";  python3 -I "$here/chain_probe.py" "$out/chain-mut/tb/srp_stream_fsms/sim_main.cpp"
python3 -I "$here/make_r3_mutants.py" "$out/chain-mut" rv3-done-before-rewalk
export_to "$head" "$out/camp"
suite order-head & suite order-mut & suite chain-mut &
( cd "$out/camp" && timeout 3000 python3 -I tb/srp_top/mutants.py --output "$out/camp-out" --jobs 8 --only \
listener-rider-not-quiet,listener-park-never-retires,listener-retire-skips-group-mark,\
listener-csid-flops-ignores-park,lsid-flops-read-sink-0,listener-walk-ends-owing-a-transmit,\
listener-walk-marks-only-served-slots,listener-walk-marks-group-only-on-retire,\
listener-repark-takes-matcher-pairs,listener-two-parks-grouped > "$out/camp.log" 2>&1; echo $? > "$out/camp.rc" ) &
wait
for n in order-head order-mut chain-mut camp; do printf '%-12s rc=%s\n' "$n" "$(cat "$out/$n.rc")"; done
grep -h -E "SUMMARY|^[0-9]+ checks:" "$out/order-head.log" "$out/order-mut.log" "$out/chain-mut.log"
tail -20 "$out/camp.log"
