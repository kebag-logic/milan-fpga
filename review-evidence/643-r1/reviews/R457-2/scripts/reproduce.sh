#!/bin/sh
# R457-2 reproduction recipe for #643 / PR #648 at head
# 6b96391d13c5d777a98b1c7be9265c63d651c911. Every step runs in a disposable
# copy under $PKT/scratch; nothing is committed or pushed.
#
#   PKT   the review packet directory (holds scripts/ and receipts/)
#   SRC   a clean checkout of 6b96391d with submodules initialised
#   V     the pinned Verilator 5.050 executable
#   MK    a GNU make 4.3 directory, first on PATH (the nested $(MAKE) and the
#         mutant runner's "make" both resolve to it)
#   EVID  the public evidence tree review-evidence/643-r1 at 531abe2b
#
# usage: reproduce.sh trees|launch1|probes|launch2|launch3|analyse
# Each launch step starts its jobs detached, one log and one rc file each,
# and returns; wait for the rc files in the foreground.
set -eu
: "${PKT:?}" "${SRC:?}" "${V:?}" "${MK:?}" "${EVID:?}"
W="$PKT/scratch"
R="$PKT/receipts"
export PATH="$MK:$PATH" VERILATOR="$V" VERILATOR_JOBS=4
SUITE=tb/verilator/milan_dp_render
STD=0,130,260,391,521,651,781,911,927,1042,1156,1172,1302,1432,1562,1693,1823,1953

bg() { # bg NAME DIR CMD...: run CMD in DIR detached, timing it
  n=$1; d=$2; shift 2
  ( cd "$d" && s=$(date +%s); rc=0; "$@" > "$R/$n.log" 2>&1 || rc=$?
    echo "wall_s=$(( $(date +%s) - s ))" >> "$R/$n.log"; echo $rc > "$R/$n.rc" ) \
    < /dev/null > /dev/null 2>&1 &
}

case "$1" in
trees)
  # head (dev pin 631eeb34), and the c4cb84ff scratch parent with the two
  # adoption patches the executor published, never committed
  rsync -a "$SRC/" "$W/head/"
  rsync -a "$SRC/" "$W/c4/"
  ( cd "$W/c4" && { git update-index -q --refresh || true; }
    git -C protocol-processor checkout -q c4cb84ff8cecad19bedaa85dde594a8ed68012f6
    git update-index --cacheinfo 160000,c4cb84ff8cecad19bedaa85dde594a8ed68012f6,protocol-processor
    git apply --index "$EVID/author/parent-adoption-c8-bbf704ec.patch"
    git apply --index "$EVID/author/parent-adoption-p2-p1-1269cdaf.patch" )
  for t in head c4; do
    for c in lb mut; do rsync -a "$W/$t/" "$W/$t-$c/"; done
  done ;;
launch1)
  # 1. the suite's default target, cold, at both processors
  # 2. the boundary-band diagnostic target, at both processors
  # 3. the campaign's own two setpoint arms through plant/build/run_leg/verdict
  for t in head c4; do
    bg "suite-$t" "$W/$t" make -C $SUITE
    # under make -C the runner's nested make prints "Entering directory" into
    # the source list and the defect builds fail (the pre-existing defect the
    # executor reports; TESTING.md says to run it from the suite directory):
    # recorded once as receipts/lb-$t-makeC.*, then run as documented
    bg "lb-$t" "$W/$t-lb/$SUITE" make tdm8render-law-boundary LAW_BOUNDARY_JOBS=4
    ( cd "$W/$t-mut/$SUITE" && make -s ltn_rom.hex ucode.hex tdm8r_aemi.bin )
    for a in sp-low sp-high; do
      bg "arm-$t-$a" "$W/$t-mut" python3 "$PKT/scripts/law_arm.py" $SUITE \
         "$W/$t-mut-work-$a" $a "$R/arm-$t-$a.leg.log"
    done
  done ;;
probes)
  # the instrumented probe (RTL nets marked public_flat_rd, no logic change;
  # LAW_PHASES / LAW_NODWELL read by the leg) and the setpoint -1 / +1 probes
  # built on top of it
  rsync -a "$SRC/" "$W/head-probe/"
  ( cd "$W/head-probe" && git apply "$PKT/scripts/probe-instrument.patch" )
  for s in sp sphi; do
    rsync -a "$W/head-probe/" "$W/head-probe-$s/"
  done
  ( cd "$W/head-probe-sp" && git apply "$PKT/scripts/probe-setpoint-minus-one.patch" )
  ( cd "$W/head-probe-sphi" && git apply "$PKT/scripts/probe-setpoint-plus-one.patch" )
  for t in head-probe head-probe-sp head-probe-sphi; do
    bg "build-$t" "$W/$t/$SUITE" make -s tdm8render-build
  done ;;
launch2)
  # 4. the probe runs: my round-1 histories, unchanged, and the setpoint probes
  run() { bg "probe-$1" "$W/$2/$SUITE" env $3 ./obj_tdm8r/Vmilan_dp_tdm8r --law-only; }
  run stdhist  head-probe      "LAW_PHASES=$STD"
  run tiehist  head-probe      "LAW_PHASES=2023,2024,2025,2026,2027,2028,2025,2025"
  run tiealone head-probe      "LAW_PHASES=2025"
  run nodwell  head-probe      "LAW_NODWELL=1 LAW_PHASES=$STD"
  run sp-std   head-probe-sp   "LAW_PHASES=$STD,2025,2026"
  run sphi-std head-probe-sphi "LAW_PHASES=$STD,2025,2026"
  # 5. an interleaved history the runner's three do not take: the band
  #    +2005..+2045 from both edges inward, in --law-boundary mode
  IL=2005,2045,2006,2044,2007,2043,2008,2042,2009,2041,2010,2040,2011,2039,2012,2038,2013,2037,2014,2036,2015,2035,2016,2034,2017,2033,2018,2032,2019,2031,2020,2030,2021,2029,2022,2028,2023,2027,2024,2026,2025
  for t in head-probe head-probe-sp head-probe-sphi; do
    bg "il-$t" "$W/$t/$SUITE" ./obj_tdm8r/Vmilan_dp_tdm8r --law-boundary=$IL
  done ;;
launch3)
  # 6. clean --law-only at both processors (the margin of 48, and the probe
  #    build's [LAW] lines compared byte for byte against it)
  for t in head c4; do
    bg "lawonly-$t" "$W/$t/$SUITE" ./obj_tdm8r/Vmilan_dp_tdm8r --law-only
  done
  # 7. the window wider than a tick (kLawGuardCycles 2100): every standing
  #    window, the 18 [LAW] phases and the CRF one, must fail "gradable"
  rsync -a "$SRC/" "$W/head-wfault/"
  ( cd "$W/head-wfault" && git apply "$PKT/scripts/probe-window-wider-than-a-tick.patch"
    cd $SUITE && make -s tdm8render-build )
  bg probe-wfault-full "$W/head-wfault/$SUITE" ./obj_tdm8r/Vmilan_dp_tdm8r
  # 8. the sound design's --law-boundary leg in the three histories, at both
  #    processors, keeping every leg's output (receipts/hist/)
  JOBS=8 "$PKT/scripts/histories.sh" ;;
analyse)
  cd "$R"
  python3 "$PKT/scripts/judge_test.py" "$W/head/$SUITE" > judge-test.log 2>&1 || true
  for t in head-probe:sound head-probe-sp:defect head-probe-sphi:defect; do
    python3 "$PKT/scripts/judge_il.py" "${t##*:}" "il-${t%%:*}.log" > "il-${t%%:*}.judge.tsv" || true
  done
  python3 "$PKT/scripts/hist_summary.py" hist > hist-summary.tsv
  python3 "$PKT/scripts/walks.py" suite-head.log suite-c4.log lawonly-head.log \
    lawonly-c4.log arm-*.leg.log probe-stdhist.log probe-tiehist.log \
    probe-tiealone.log probe-sp-std.log probe-sphi-std.log hist/*.log > walks.tsv ;;
*) echo "usage: $0 trees|launch1|probes|launch2|launch3|analyse" >&2; exit 2 ;;
esac
