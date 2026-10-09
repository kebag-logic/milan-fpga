#!/bin/sh
# The focused runs of review R474-4 at 85db353400c6bf3965d279a9f5b5d47e08a0d1ed,
# as executed (each was started in the background with its own log and rc file).
# Usage: run_focused.sh <clone at the head> <out dir> <verilator 5.050>
# EXPORT is a `git archive` export of the head plus its three submodules; the
# render and physical legs need git (pp_srcs.py) and ran in the clone itself.
set -u
R=${1:?clone}; O=${2:?out}; V=${3:?verilator}
EXPORT=${EXPORT:-$O/head-export}
mkdir -p "$O"
run() { n=$1; shift; ( "$@" > "$O/$n.log" 2>&1; echo $? > "$O/$n.rc" ); }
# follow_ring: b8, pullin, small pulls, controller at four rates, 12 controls
run follow_ring make -C "$EXPORT/tb/verilator/follow_ring" all VERILATOR="$V" \
    VERILATOR_JOBS=4 SWEEP_JOBS=4 MDIR="$O/fr_obj"
# capture ring: [LRC], span checks, netlist leg
run chmap_capture make -C "$EXPORT/tb/verilator/chmap_capture" all VERILATOR="$V" VERILATOR_JOBS=4
# two arrival-campaign runs, byte-compared with the author's published logs
run arrival_slow_none_p00 "$O/fr_obj/Vfollow_ring" --case b8 --set-phase 0.000000 --jitter-us 0 \
    --tail-us 0 --tail-p 0 --hold-s 40 --switch-hold-s 20 --latency-us 200 --seed 645 \
    --allow-ungradable --peer-ppm -11.02 --dwell-s 1
run arrival_fast_uniform60_p05 "$O/fr_obj/Vfollow_ring" --case b8 --set-phase 0.312500 --jitter-us 60 \
    --tail-us 0 --tail-p 0 --hold-s 40 --switch-hold-s 20 --latency-us 200 --seed 650 \
    --allow-ungradable --peer-ppm 0.82 --dwell-s 45
# render pull-in, LAW boundary and the full #657 mutation campaign (in the clone)
run head_render_pullin make -C "$R/tb/verilator/milan_dp_render" tdm8render-pullin VERILATOR="$V" \
    VERILATOR_JOBS=6 PULLIN_JOBS=6
run head_render_lawb make -C "$R/tb/verilator/milan_dp_render" tdm8render-law-boundary VERILATOR="$V" \
    VERILATOR_JOBS=6 LAW_BOUNDARY_JOBS=8
run head_render_mutants make -C "$R/tb/verilator/milan_dp_render" tdm8render-mutants VERILATOR="$V" \
    VERILATOR_JOBS=8
# physical gPTP leg: main, abort, accounting and recentre controls (in the clone)
run head_physical_gptp make -C "$R/tb/verilator/milan_dp_gptp" all VERILATOR="$V" VERILATOR_JOBS=4
