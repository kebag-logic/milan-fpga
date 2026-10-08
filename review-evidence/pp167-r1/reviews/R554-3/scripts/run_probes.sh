#!/usr/bin/env bash
# R554-3 probes: Q1 SC2 cancel-clock log (scratch copy), Q2 the two SC mutant arms
# usage: run_probes.sh <packet>   (needs scratch/head from run_gates.sh)
set -u
P=$1; V=${VERILATOR:?set VERILATOR to the pinned Verilator 5.050 wrapper}; R=$P/receipts
Q=$P/scratch/probe; rm -rf "$Q"; cp -a "$P/scratch/head" "$Q"; rm -rf "$Q"/tb/aecp_notify/obj_*
python3 -I "$P/scripts/probe_sc2_clock.py" "$Q/tb/aecp_notify/sim_main.cpp"
mkdir -p "$P/scratch/tmp" "$P/scratch/mut"
( cd "$Q/tb/aecp_notify" && make VERILATOR="$V" failure-window > "$R/probe_q1_sc2_clock.log" 2>&1; echo $? > "$R/probe_q1_sc2_clock.rc" ) &
( cd "$P/scratch/head" && TMPDIR="$P/scratch/tmp" python3 -I tb/pp_top/notify_mutants.py --output "$P/scratch/mut" \
    --verilator "$V" --jobs 4 --only cancel_collision_drops_command cancel_pending_accepts_failure \
    > "$R/probe_q2_sc_mutants.log" 2>&1; echo $? > "$R/probe_q2_sc_mutants.rc"; cp "$P/scratch/mut/results.json" "$R/probe_q2_sc_mutants_results.json" ) &
wait
