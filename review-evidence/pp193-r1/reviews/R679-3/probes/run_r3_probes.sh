#!/bin/sh
# Round-3 reviewer probes on a processor clone, never touching it.
# usage: run_r3_probes.sh <clone> <head> <round-base> <outdir> [parallel]
# Needs Verilator 5.050 (the CI pin) as `verilator` on PATH. Each job exports
# a revision with `git archive` into <outdir>/<job>, runs in it, and leaves
# <outdir>/<job>.log and <outdir>/<job>.rc.
#   head-full     head, tb/srp_stream_fsms `make` (walk arms + suite)
#   s2-head       s2_probe.py at head      s2-base   at the round base
#   repark-head   repark_probe.py at head  repark-mut  with the re-park edit
#   chain-head    chain_probe.py at head   chain-base  at the round base
#   tests-on-base head's stream-FSM suite on the round base's listener RTL
#   rv3-*         make_r3_mutants.py arms, head suite
#   ctl-*         the author's five new controls, applied with git apply
set -u
clone=$1; head=$2; base=$3; out=$4; par=${5:-6}
here=$(cd "$(dirname "$0")" && pwd)
mkdir -p "$out"
export_to() { rm -rf "$2"; mkdir -p "$2"; git -C "$clone" archive "$1" | tar -x -C "$2"; }

job() {
  n=$1; d="$out/$n"
  case $n in
    head-full)     export_to "$head" "$d" ;;
    s2-head)       export_to "$head" "$d"; python3 -I "$here/s2_probe.py" "$d/tb/srp_stream_fsms/sim_main.cpp" ;;
    s2-base)       export_to "$base" "$d"; python3 -I "$here/s2_probe.py" "$d/tb/srp_stream_fsms/sim_main.cpp" ;;
    repark-head)   export_to "$head" "$d"; python3 -I "$here/repark_probe.py" "$d/tb/srp_stream_fsms/sim_main.cpp" ;;
    repark-mut)    export_to "$head" "$d"; python3 -I "$here/repark_probe.py" "$d/tb/srp_stream_fsms/sim_main.cpp"
                   (cd "$d" && patch -s -p1 --fuzz=0 < "$here/rv-repark-overwrites-pairs.patch") || { echo 97 > "$out/$n.rc"; return; } ;;
    chain-head)    export_to "$head" "$d"; python3 -I "$here/chain_probe.py" "$d/tb/srp_stream_fsms/sim_main.cpp" ;;
    chain-base)    export_to "$base" "$d"; python3 -I "$here/chain_probe.py" "$d/tb/srp_stream_fsms/sim_main.cpp" ;;
    tests-on-base) export_to "$head" "$d"
                   git -C "$clone" show "$base:hdl/srp/KL_srp_listener_fsm.sv" > "$d/hdl/srp/KL_srp_listener_fsm.sv" ;;
    rv3-*)         export_to "$head" "$d"; python3 -I "$here/make_r3_mutants.py" "$d" "$n" ;;
    ctl-*)         export_to "$head" "$d"
                   (cd "$d" && git apply --check "tb/srp_top/mutations/${n#ctl-}.patch" \
                            && git apply "tb/srp_top/mutations/${n#ctl-}.patch") || { echo 98 > "$out/$n.rc"; return; } ;;
  esac
  if [ "$n" = head-full ]; then args=""; else args="RUN_ARGS=suite"; fi
  ( cd "$d/tb/srp_stream_fsms" && timeout 1500 make $args > "$out/$n.log" 2>&1; echo $? > "$out/$n.rc" )
}

jobs="head-full s2-head s2-base repark-head repark-mut chain-head chain-base tests-on-base \
rv3-group-mark-on-lo rv3-done-before-rewalk rv3-rewalk-keeps-wsrc rv3-take-keeps-taker-mark \
ctl-listener-walk-ends-owing-a-transmit ctl-listener-walk-marks-only-served-slots \
ctl-listener-walk-marks-group-only-on-retire ctl-listener-repark-takes-matcher-pairs \
ctl-listener-two-parks-grouped"
i=0
for n in $jobs; do
  job "$n" &
  i=$((i+1))
  if [ $((i % par)) -eq 0 ]; then wait; fi
done
wait
for n in $jobs; do printf '%-48s rc=%s  %s\n' "$n" "$(cat "$out/$n.rc" 2>/dev/null)" "$(grep -E '^[0-9]+ checks:' "$out/$n.log" 2>/dev/null | tail -1)"; done
