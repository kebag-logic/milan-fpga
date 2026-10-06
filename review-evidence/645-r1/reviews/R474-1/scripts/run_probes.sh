#!/bin/sh
# R474-1 reviewer probes for PR #672 at 4e1ddee9d7b9ebf58ebebcacd90c5d72dce0c96f.
# Disposable: every build and log lands under $WORK; the candidate tree is
# only read. Needs Verilator 5.050 on PATH.
#
#   CAND=/path/to/candidate WORK=/path/to/scratch sh run_probes.sh
#
# Probe A (full side): follow_ring's own b8 leg with the offset sign reversed
#   (peer +0.82 ppm against gPTP, DUT INTERNAL -5.10 ppm, so the DUT reads
#   5.92 ppm SLOW and its loopback ring parks at the full edge during a long
#   INTERNAL dwell). The shipped harness and model are unchanged.
# Probe B (sub-threshold pull): a copy of follow_ring with a 1/64-sample
#   serial-clock quantum (audio 3.072 MHz, FRAME_DIV_P 64) at a 25 MHz axis
#   clock (the wrapper scales the aligner's gains), so a hold can pull the
#   grid by 3/64 sample, under the 1/16-sample excursion arm.
set -eu
: "${CAND:?candidate checkout}" "${WORK:?scratch directory}"
mkdir -p "$WORK/probe"

# ---- Probe A ---------------------------------------------------------------
make -C "$CAND/tb/verilator/follow_ring" build MDIR="$WORK/fr_model" VERILATOR_JOBS=4
A="$WORK/fr_model/Vfollow_ring"
( cd "$WORK/probe" && { "$A" --case b8 --peer-ppm 0.82 --dwell-s 45 --set-phase 0.0 --hold-s 20 \
    > fullside_j0.log 2>&1; echo $? > fullside_j0.rc; } ) &
( cd "$WORK/probe" && { "$A" --case b8 --peer-ppm 0.82 --dwell-s 45 --set-phase 0.0 --hold-s 20 \
    --jitter-us 60 --seed 645 > fullside_j60.log 2>&1; echo $? > fullside_j60.rc; } ) &
# four more set instants across one beat (the harness's --set-phase waits for
# a dup, and a ring at its full edge only skips, so the dwell moves the set)
for d in 45.44 46.32 47.20 48.08; do
  ( cd "$WORK/probe" && { "$A" --case b8 --peer-ppm 0.82 --dwell-s "$d" --set-phase 0.0 --hold-s 20 \
      > "fullside_j0_d$d.log" 2>&1; echo $? > "fullside_j0_d$d.rc"; } ) &
done

# ---- Probe B0: the shipped harness quantises a hold to 1/16 sample ----------
# small_*: +-1/16 sample (arms); sub_*: whole frames (no pull at all)
for h in 40.6 42.7; do for lat in 184.6 205.9; do
  ( cd "$WORK/probe" && { "$A" --case pullin --hold-us "$h" --latency-us "$lat" --after-s 1.5 \
      > "small_h${h}_l$lat.log" 2>&1; echo $? > "small_h${h}_l$lat.rc"; } ) &
done; done
for h in 41.1 42.24; do for lat in 205.9 225.3; do
  ( cd "$WORK/probe" && { "$A" --case pullin --hold-us "$h" --latency-us "$lat" --after-s 1.5 \
      --grid-trace "sub_h${h}_l$lat.grid.csv" > "sub_h${h}_l$lat.log" 2>&1; \
      echo $? > "sub_h${h}_l$lat.rc"; } ) &
done; done

# ---- Probe B ---------------------------------------------------------------
P="$WORK/ptree"
rm -rf "$P"; mkdir -p "$P/tb/verilator"
ln -s "$CAND/hdl" "$P/hdl"; ln -s "$CAND/configs" "$P/configs"
ln -s "$CAND/tb/common" "$P/tb/common"
ln -s "$CAND/tb/verilator/mmcm_servo" "$P/tb/verilator/mmcm_servo"
cp -r "$CAND/tb/verilator/follow_ring" "$P/tb/verilator/follow_ring"
sed -i 's|^constexpr double kAudioHz = 24.576e6 / 32.0;|constexpr double kAudioHz = 24.576e6 / 8.0;  // PROBE: 1/64-sample hold quantum|' \
    "$P/tb/verilator/follow_ring/sim_main.cpp"
make -C "$P/tb/verilator/follow_ring" build MDIR="$P/m25" CLK_HZ=25000000 VERILATOR_JOBS=4 \
    MUT_DEFS=-GFRAME_DIV_P=64
B="$P/m25/Vfollow_ring"
# 42.64 us = 131 audio cycles = 2 frames + 3/64 sample (under the arm):
# fine_* sit clear of the 9-tick boundary, cross_* just inside it
for lat in 205.4 205.8 206.2; do
  ( cd "$WORK/probe" && { "$B" --case pullin --hold-us 42.64 --latency-us "$lat" --after-s 1.5 \
      --grid-trace "fine_h42.64_l$lat.grid.csv" > "fine_h42.64_l$lat.log" 2>&1; \
      echo $? > "fine_h42.64_l$lat.rc"; } ) &
done
for lat in 204.2 204.4 204.6; do
  ( cd "$WORK/probe" && { "$B" --case pullin --hold-us 42.64 --latency-us "$lat" --after-s 1.5 \
      > "cross_h42.64_l$lat.log" 2>&1; echo $? > "cross_h42.64_l$lat.rc"; } ) &
done
# control: 43.29 us = 133 audio cycles = 2 frames + 5/64 sample (over the arm)
( cd "$WORK/probe" && { "$B" --case pullin --hold-us 43.29 --latency-us 204.4 --after-s 1.5 \
    --grid-trace ctl_h43.29_l204.4.grid.csv > ctl_h43.29_l204.4.log 2>&1; \
    echo $? > ctl_h43.29_l204.4.rc; } ) &
wait
grep -H -e RESULT -e FAIL -e 'checks:' "$WORK"/probe/*.log
