#!/usr/bin/env bash
# usage: order_probes.sh <clone> <head> <out>: R679-3's order_probe.py on a
# copy of the head's suite, at the head and with the round's named control
# (the committed patch listener-walk-done-before-second-pass) and with
# R679-3's own arm rv3-done-before-rewalk (make_r3_mutants.py), one build at a time
set -u
clone=$1; head=$2; out=$3
P=<scratch>/r4/probes/r679-3
. <scratch>/r4/scripts/env.sh
mkdir -p "$out"
export_to() { rm -rf "$out/$1"; mkdir -p "$out/$1"; git -C "$clone" archive "$head" | tar -x -C "$out/$1"; }
suite() { ( cd "$out/$1/tb/srp_stream_fsms" && timeout 1500 make RUN_ARGS=suite > "$out/$1.log" 2>&1; echo $? > "$out/$1.rc" ); }
export_to order-head; python3 -I $P/order_probe.py "$out/order-head/tb/srp_stream_fsms/sim_main.cpp"
export_to order-ctl;  python3 -I $P/order_probe.py "$out/order-ctl/tb/srp_stream_fsms/sim_main.cpp"
( cd "$out/order-ctl" && git apply tb/srp_top/mutations/listener-walk-done-before-second-pass.patch ) && echo "planted listener-walk-done-before-second-pass"
export_to order-rv3;  python3 -I $P/order_probe.py "$out/order-rv3/tb/srp_stream_fsms/sim_main.cpp"
python3 -I $P/make_r3_mutants.py "$out/order-rv3" rv3-done-before-rewalk
for n in order-head order-ctl order-rv3; do suite $n; done
for n in order-head order-ctl order-rv3; do printf '%-11s rc=%s ' $n "$(cat $out/$n.rc)"; grep -h -E "SUMMARY|^[0-9]+ checks:" "$out/$n.log" | tr '\n' ' '; echo; done > "$out/SUMMARY.txt"
echo done > "$out/ALL.done"
