#!/bin/bash
# R474-2 command record (portable). Every command ran in the foreground from a
# `git archive` export of 886e16201654ba0fd0c60c41c228ea4c75b2f6d3 at $SRC; builds and
# planted copies live under $SCR (never published). V is Verilator 5.050.
set -euo pipefail
: "${SRC:?export of the head}" "${SCR:?scratch dir}" "${V:?verilator 5.050}" "${PROBES:?this directory}"
FR=$SRC/tb/verilator/follow_ring
# head builds of follow_ring at four axis clocks (FRAME_DIV 64 default)
for hz in 6250000 25000000 50000000 100000000; do
  make -C $FR build VERILATOR=$V VERILATOR_JOBS=8 CLK_HZ=$hz MDIR=$SCR/fr$hz; done
# quiet distributions / zero false fires (receipts/quiet)
$SCR/fr6250000/Vfollow_ring --case b8 --dwell-s 1.0 --set-phase 0.0 --hold-s 16 --switch-hold-s 15
$SCR/fr25000000/Vfollow_ring --case b8 --dwell-s 1.0 --set-phase 0.0 --hold-s 13 --grid-trace q25slow.csv
$SCR/fr25000000/Vfollow_ring --case b8 --dwell-s 1.0 --set-phase 0.5 --peer-ppm 0.82 --hold-s 13 --grid-trace q25fast.csv
$SCR/fr25000000/Vfollow_ring --case b8 --dwell-s 1.0 --set-phase 0.25 --jitter-us 60 --seed 700 --hold-s 13 --allow-ungradable
$SCR/fr25000000/Vfollow_ring --case b8 --dwell-s 1.0 --set-phase 0.75 --peer-ppm 0.82 --jitter-us 60 --seed 701 --hold-s 13 --allow-ungradable
$SCR/fr25000000/Vfollow_ring --case b8 --dwell-s 1.0 --set-phase 0.5 --jitter-us 2 --tail-us 24 --tail-p 1e-4 --seed 702 --hold-s 13 --allow-ungradable
$SCR/fr50000000/Vfollow_ring --case pullin --hold-us 0 --latency-us 204.4 --after-s 3
timeout 585 $SCR/fr50000000/Vfollow_ring --case b8 --dwell-s 1.0 --set-phase 0.0 --hold-s 16 --grid-trace q50.csv || true   # partial (wall limit)
timeout 585 $SCR/fr100000000/Vfollow_ring --case b8 --dwell-s 1.0 --set-phase 0.0 --hold-s 16 --grid-trace q100.csv || true # partial
python3 $PROBES/grid_hist.py q50.csv 15.3 16.9   # and the other windows in receipts/quiet/grid_trace_histograms.txt
# recovery window and settle latency per clock (receipts/recovery)
for hz in 6250000 50000000; do for h in 52 56; do
  $SCR/fr$hz/Vfollow_ring --case pullin --hold-us $h --latency-us 210.42 --after-s 3 --allow-ungradable; done; done
for h in 52 56; do $SCR/fr100000000/Vfollow_ring --case pullin --hold-us $h --latency-us 210.42 --after-s 2.5 --allow-ungradable; done
# INTERNAL pull-in campaign, 52 and 56 us (receipts/sweeps)
for h in 52 56; do (cd $FR && python3 sweep.py pullin --exe $SCR/fr6250000/Vfollow_ring --out $SCR/sw$h --jobs 4 --hold-us $h); done
# head standing legs (receipts/head)
make -C $SRC/tb/verilator/chmap_capture build VERILATOR=$V VERILATOR_JOBS=8 MDIR=$SCR/head/cmap_obj && $SCR/head/cmap_obj/Vchmap_wrap
(cd $FR && python3 small_pulls.py --exe $SCR/fr25000000/Vfollow_ring --out $SCR/head/small --jobs 4)
# probe P1: a declared hold visiting a still-empty pair (receipts/probe_p1)
cp -r $SRC/tb/verilator/chmap_capture $SRC/tb/verilator/chmap_capture_p1
python3 $PROBES/probe_lrc_empty_hold.py $SRC/tb/verilator/chmap_capture_p1/sim_main.cpp
make -C $SRC/tb/verilator/chmap_capture_p1 build VERILATOR=$V VERILATOR_JOBS=8 && $SRC/tb/verilator/chmap_capture_p1/obj_dir/Vchmap_wrap
rm -rf $SRC/tb/verilator/chmap_capture_p1   # it would otherwise perturb the traceability check
# reviewer plants (receipts/plants)
python3 $PROBES/r474_plants.py $SRC $SCR/m NODROP NOHOLD HOLDDUP DROPSKIP BAND1 BAND8 REARM64 REARM512
for n in NODROP NOHOLD HOLDDUP DROPSKIP; do $PROBES/r474_run_cmap.sh $SCR/m/$n $V; done
for n in BAND1 BAND8 REARM64 REARM512; do
  (cd $SCR/m/$n/tb/verilator/follow_ring && python3 settle_control.py --sim $V --out $SCR/m/$n/control --jobs 2); done
make -C $SCR/m/BAND1/tb/verilator/follow_ring build VERILATOR=$V CLK_HZ=25000000 MDIR=$SCR/m/BAND1/fr25
make -C $SCR/m/BAND1/tb/verilator/follow_ring build VERILATOR=$V MDIR=$SCR/m/BAND1/fr625
make -C $SCR/m/REARM64/tb/verilator/follow_ring build VERILATOR=$V CLK_HZ=25000000 MDIR=$SCR/m/REARM64/fr25
$SCR/m/BAND1/fr25/Vfollow_ring --case pullin --hold-us 0 --latency-us 204.4 --after-s 1.5
$SCR/m/BAND1/fr625/Vfollow_ring --case b8 --dwell-s 1.0 --set-phase 0.0 --hold-s 16 --switch-hold-s 15
$SCR/m/BAND1/fr25/Vfollow_ring --case pullin --hold-us 42.64 --latency-us 204.4 --after-s 1.5
$SCR/m/REARM64/fr25/Vfollow_ring --case pullin --hold-us 42.64 --latency-us 204.4 --after-s 1.5
$SCR/m/REARM64/fr25/Vfollow_ring --case pullin --hold-us 42.64 --latency-us 204.4 --after-s 1.5 \
  --second-after-action-s 0.10 --second-hold-us 40.690104167 --second-inside-recovery
$SCR/m/REARM64/fr25/Vfollow_ring --case pullin --hold-us 44.270833333 --latency-us 210.42 --after-s 1.5
# read-only gates in the review checkout (receipts/gates)
python3 scripts/lint_rtl.py --check; python3 scripts/check_doc_style.py; python3 scripts/check_doc_paths.py
python3 scripts/check_rtl_source_lists.py; python3 docs/traceability/gen_module_matrix.py --check
python3 scripts/check_sv_idiom.py; python3 scripts/check_py_idiom.py
python3 scripts/check_em_dash.py --base 09f1841bd2c6a9dea8eb1994d887f7386ca4f62d   # could not judge here (renderer absent)
# merge audit in a --shared scratch clone: git merge-tree --write-tree <lane> <dev> vs the merge's tree (receipts/merges.txt)
# restoration: python3 $PROBES/verify_checkout.py <checkout> f2eb9b9b... protocol-processor=ead80360... gptp-processor=5dce647a... third_party/verilog-axis=48ff7a7e...
