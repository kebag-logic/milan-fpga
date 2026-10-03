#!/bin/sh
# R457-1 reproduction recipe for #643 / PR #648 at head 98729742b71d5088f250440eb46085daf1c0cbdb.
# Every step runs in a disposable copy; nothing is committed or pushed.
#
#   PKT   the review packet directory (holds scripts/ and receipts/)
#   SRC   a clean checkout of 98729742 with submodules initialised
#   V     the pinned Verilator 5.050 executable
#   MK    a GNU make 4.3 directory, first on PATH (the nested $(MAKE) and the
#         mutant runner's "make" both resolve to it)
#   EVID  the public evidence tree review-evidence/643-r1 at 531abe2b
set -eu
: "${PKT:?}" "${SRC:?}" "${V:?}" "${MK:?}" "${EVID:?}"
W="$PKT/scratch"
export PATH="$MK:$PATH" VERILATOR="$V"
STD=0,130,260,391,521,651,781,911,927,1042,1156,1172,1302,1432,1562,1693,1823,1953

# 1. the two trees: head (dev pin 631eeb34), and the c4cb84ff scratch parent
rsync -a "$SRC/" "$W/head/"
rsync -a "$SRC/" "$W/c4/"
( cd "$W/c4" && git update-index -q --refresh || true
  git -C protocol-processor checkout -q c4cb84ff8cecad19bedaa85dde594a8ed68012f6
  git update-index --cacheinfo 160000,c4cb84ff8cecad19bedaa85dde594a8ed68012f6,protocol-processor
  git apply --index "$EVID/author/parent-adoption-c8-bbf704ec.patch"
  git apply --index "$EVID/author/parent-adoption-p2-p1-1269cdaf.patch" )

# 2. the suite's default target, cold, at both processors (run concurrently)
for t in head c4; do
  ( cd "$W/$t" && make -C tb/verilator/milan_dp_render VERILATOR="$V" \
      > "$PKT/receipts/suite-$t.log" 2>&1; echo $? > "$PKT/receipts/suite-$t.rc" ) &
done
wait

# 3. the campaign's own A2-a arm and its --law-only positive control, through
#    the runner's plant/build/run_leg/verdict, at both processors
for t in head c4; do
  rsync -a "$W/$t/" "$W/$t-mut/"
  ( cd "$W/$t-mut/tb/verilator/milan_dp_render" && make -s ltn_rom.hex ucode.hex tdm8r_aemi.bin )
  for a in clean a2a; do
    ( cd "$W/$t-mut" && python3 "$PKT/scripts/law_arm.py" tb/verilator/milan_dp_render \
        "$W/$t-mut-work-$a" "$a" "$PKT/receipts/law-$t-$a.leg.log" \
        > "$PKT/receipts/law-$t-$a.out" 2>&1; echo $? > "$PKT/receipts/law-$t-$a.rc" ) &
  done
done
wait

# 4. the tuple verdict and the phase table, offline
python3 "$PKT/scripts/verdict_tuple_test.py" "$SRC/tb/verilator/milan_dp_render"

# 5. the instrumented probe (three RTL nets marked public_flat_rd, no logic
#    change; LAW_PHASES / LAW_NODWELL read by the leg), and the setpoint-7
#    probe built on top of it
rsync -a "$SRC/" "$W/head-probe/"
( cd "$W/head-probe" && git apply "$PKT/scripts/probe-instrument.patch" )
rsync -a "$W/head-probe/" "$W/head-probe-sp/"
( cd "$W/head-probe-sp" && git apply "$PKT/scripts/probe-setpoint-minus-one.patch" )
for t in head-probe head-probe-sp; do
  ( cd "$W/$t/tb/verilator/milan_dp_render" && make -s tdm8render-build ) &
done
wait
run() { ( cd "$W/$2/tb/verilator/milan_dp_render" && env $3 ./obj_tdm8r/Vmilan_dp_tdm8r --law-only \
          > "$PKT/receipts/probe-$1.log" 2>&1; echo $? > "$PKT/receipts/probe-$1.rc" ) & }
run stdhist  head-probe    "LAW_PHASES=$STD"
run tiehist  head-probe    "LAW_PHASES=2023,2024,2025,2026,2027,2028,2025,2025"
run tiealone head-probe    "LAW_PHASES=2025"
run nodwell  head-probe    "LAW_NODWELL=1 LAW_PHASES=$STD"
run sp-std   head-probe-sp "LAW_PHASES=$STD,2025,2026"
wait
