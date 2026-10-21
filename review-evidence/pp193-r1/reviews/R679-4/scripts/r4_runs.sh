#!/usr/bin/env bash
# usage: r4_runs.sh <clone> <head> <packet>
# Exports the head into disposable trees under <packet>/scratch/runs, plants
# probes/controls in the copies only, and runs the stream-FSM suite in each,
# plus the srp_top campaign arms whose rows changed this round, concurrently.
set -u
clone=$1; head=$2; pk=$3
S=$pk/scratch/runs; R=$pk/receipts/runs
rm -rf "$S"; mkdir -p "$S" "$R"
export VERILATOR=$pk/scratch/vwrap TMPDIR=$pk/scratch/tmp PYTHONDONTWRITEBYTECODE=1
mkdir -p "$TMPDIR"
ex() { mkdir -p "$S/$1"; git -C "$clone" archive "$head" | tar -x -C "$S/$1"; }
cpp() { echo "$S/$1/tb/srp_stream_fsms/sim_main.cpp"; }
pl() { ( cd "$S/$1" && git apply --check "tb/srp_top/mutations/$2.patch" && git apply "tb/srp_top/mutations/$2.patch" ) && echo "planted $2 in $1"; }
for t in head-full head-order ctl-order rider-mut rider-novo-mut rider-probe-head rider-probe-mut camp; do ex $t; done
python3 -I $pk/probes/order_probe.py "$(cpp head-order)"
python3 -I $pk/probes/order_probe.py "$(cpp ctl-order)"; pl ctl-order listener-walk-done-before-second-pass
pl rider-mut listener-rider-not-quiet
python3 -I $pk/probes/drop_sh1_vo_check.py "$(cpp rider-novo-mut)"; pl rider-novo-mut listener-rider-not-quiet
python3 -I $pk/probes/rider_probe.py "$(cpp rider-probe-head)"
python3 -I $pk/probes/rider_probe.py "$(cpp rider-probe-mut)"; pl rider-probe-mut listener-rider-not-quiet
run() { local t=$1 a=$2; ( cd "$S/$t/tb/srp_stream_fsms" && timeout 1800 make RUN_ARGS=$a > "$R/$t.log" 2>&1; echo $? > "$R/$t.rc" ) & }
run head-full ""
for t in head-order ctl-order rider-mut rider-novo-mut rider-probe-head rider-probe-mut; do run $t suite; done
( cd "$S/camp" && timeout 3000 python3 -I tb/srp_top/mutants.py --output "$R/camp-out" --jobs 6 \
   --only listener-walk-done-before-second-pass,listener-settle-compare-dropped,listener-rider-not-quiet,listener-handover-drops-state,listener-group-order-reversed,listener-handover-forgets-walk-mark,listener-walk-ends-owing-a-transmit,listener-walk-marks-group-only-on-retire \
   > "$R/camp.log" 2>&1; echo $? > "$R/camp.rc" ) &
wait
echo done > "$R/ALL.done"
