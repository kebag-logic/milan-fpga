#!/bin/sh
# run_probes.sh CHECKOUT WORK OUT - the reviewer's code probe at the head: lwSRP's Join gate removed
# (mrp_mad.c "ps->join_wait = ps->join_cs;" -> "ps->join_wait = 0;"), built through the tracked mutant
# driver's helpers, graded on wire 3000 ms, wire 40000 ms, licence and hold; and a clean control on wire 3000 ms.
set -u
H="$1/tb/verilator/milan_dp"; W="$2"; O="$3"; S="$(dirname "$0")"
VERILATOR="${VERILATOR:-verilator}"; export VERILATOR
MAKEFLAGS=-j12 python3 -B "$S/gate_probe.py" "$H" "$W/gate-off" join-gate-off wire 3000 > "$O/gate-off.log" 2>&1
for s in "wire 40000" "licence 0" "hold 0"; do
  set -- $s
  extra=""; [ "$2" != 0 ] && extra="--ms $2"
  ( cd "$H" && "$W/gate-off/sp/Vmilan_dp_twin_sp" --srptx "$1" "$W/gate-off/$1-$2.json" $extra > "$O/gate-off-$1.log" 2>&1
    python3 -B srptx_grade.py "$W/gate-off/$1-$2.json" >> "$O/gate-off-$1.log" 2>&1; echo "grade rc $?" >> "$O/gate-off-$1.log" ) &
done
wait
MAKEFLAGS=-j8 python3 -B "$S/gate_probe.py" "$H" "$W/clean" clean wire 3000 > "$O/clean.log" 2>&1
