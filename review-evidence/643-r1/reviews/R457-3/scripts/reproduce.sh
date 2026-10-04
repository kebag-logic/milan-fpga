#!/bin/sh
# R457-3 reproduction recipe for #643 / PR #648 at head
# 36207e91c81fd33782b01486e3bc2fea50e91a1e. Round 2's recipe (R457-2
# scripts/reproduce.sh) with its steps unchanged, except:
#   - probe-window-wider-than-a-tick.patch no longer applies (its context is
#     the walk line round 3 restates); its single edit, kLawGuardCycles 4 ->
#     2100, is applied by hand (step 7) and recorded as
#     scripts/probe-window-wider-than-a-tick-r3.patch;
#   - the A2-a arm runs beside the two setpoint arms in launch1;
#   - TMPDIR points into the scratch directory (the runner's work trees);
#   - new legs (launch3): the walk's wrap branch, the half-tick phases
#     +974..+994 where the nearest pop changes side; and --crf-only, at both
#     processors.
# Every step runs in a disposable copy under $PKT/scratch; nothing is
# committed or pushed.
#
#   PKT   the review packet directory (holds scripts/ and receipts/)
#   SRC   a clean checkout of 36207e91 with submodules initialised
#   V     the pinned Verilator 5.050 executable
#   MK    a GNU make 4.3 directory, first on PATH
#   EVID  the public evidence tree review-evidence/643-r1 (author/ patches)
#
# usage: reproduce.sh trees|launch1|probes|launch2|launch2b|launch3|analyse
# Each launch step starts its jobs detached, one log and one rc file each,
# and returns; wait for the rc files in the foreground.
set -eu
: "${PKT:?}" "${SRC:?}" "${V:?}" "${MK:?}" "${EVID:?}"
W="$PKT/scratch"
R="$PKT/receipts"
export PATH="$MK:$PATH" VERILATOR="$V" VERILATOR_JOBS=4 TMPDIR="$W/tmp"
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
  for t in head c4; do
    bg "suite-$t" "$W/$t" make -C $SUITE
    bg "lb-$t" "$W/$t-lb/$SUITE" make tdm8render-law-boundary LAW_BOUNDARY_JOBS=4
    ( cd "$W/$t-mut/$SUITE" && make -s ltn_rom.hex ucode.hex tdm8r_aemi.bin )
    for a in sp-low sp-high a2a; do
      bg "arm-$t-$a" "$W/$t-mut" python3 "$PKT/scripts/law_arm.py" $SUITE \
         "$W/$t-mut-work-$a" $a "$R/arm-$t-$a.leg.log"
    done
  done ;;
probes)
  rsync -a "$SRC/" "$W/head-probe/"
  ( cd "$W/head-probe" && git apply "$PKT/scripts/probe-instrument.patch" )
  for s in sp sphi; do
    rsync -a "$W/head-probe/" "$W/head-probe-$s/"
  done
  ( cd "$W/head-probe-sp" && git apply "$PKT/scripts/probe-setpoint-minus-one.patch" )
  ( cd "$W/head-probe-sphi" && git apply "$PKT/scripts/probe-setpoint-plus-one.patch" )
  for t in head-probe head-probe-sp head-probe-sphi; do
    bg "build-$t" "$W/$t/$SUITE" make -s tdm8render-build
  done
  # 7, built here: the window wider than a tick, the one edit by hand
  rsync -a "$SRC/" "$W/head-wfault/"
  ( cd "$W/head-wfault" &&
    sed -i 's/^constexpr long kLawGuardCycles = 4;$/constexpr long kLawGuardCycles = 2100;/' \
        $SUITE/sim_tdm8_render.cpp &&
    git diff > "$PKT/scripts/probe-window-wider-than-a-tick-r3.patch" )
  bg build-wfault "$W/head-wfault/$SUITE" make -s tdm8render-build ;;
launch2)
  run() { bg "probe-$1" "$W/$2/$SUITE" env $3 ./obj_tdm8r/Vmilan_dp_tdm8r --law-only; }
  run stdhist  head-probe      "LAW_PHASES=$STD"
  run tiehist  head-probe      "LAW_PHASES=2023,2024,2025,2026,2027,2028,2025,2025"
  run tiealone head-probe      "LAW_PHASES=2025"
  run nodwell  head-probe      "LAW_NODWELL=1 LAW_PHASES=$STD"
  run sp-std   head-probe-sp   "LAW_PHASES=$STD,2025,2026"
  run sphi-std head-probe-sphi "LAW_PHASES=$STD,2025,2026" ;;
launch2b)
  # split from launch2 to stay within 16 concurrent jobs
  IL=2005,2045,2006,2044,2007,2043,2008,2042,2009,2041,2010,2040,2011,2039,2012,2038,2013,2037,2014,2036,2015,2035,2016,2034,2017,2033,2018,2032,2019,2031,2020,2030,2021,2029,2022,2028,2023,2027,2024,2026,2025
  for t in head-probe head-probe-sp head-probe-sphi; do
    bg "il-$t" "$W/$t/$SUITE" ./obj_tdm8r/Vmilan_dp_tdm8r --law-boundary=$IL
  done
  bg probe-wfault-full "$W/head-wfault/$SUITE" ./obj_tdm8r/Vmilan_dp_tdm8r ;;
launch3)
  for t in head c4; do
    bg "lawonly-$t" "$W/$t/$SUITE" ./obj_tdm8r/Vmilan_dp_tdm8r --law-only
    # new: the walk's wrap branch, the phases half a tick from the boundary
    bg "wrap-$t" "$W/$t/$SUITE" ./obj_tdm8r/Vmilan_dp_tdm8r --law-boundary=974..994
    # new: --crf-only, the CRF window's place the design page cites
    bg "crfonly-$t" "$W/$t/$SUITE" ./obj_tdm8r/Vmilan_dp_tdm8r --crf-only
  done
  JOBS=${HJOBS:-8} "$PKT/scripts/histories.sh" ;;
analyse)
  cd "$R"
  python3 "$PKT/scripts/judge_test.py" "$W/head/$SUITE" > judge-test.log 2>&1 || true
  for t in head-probe:sound head-probe-sp:defect head-probe-sphi:defect; do
    python3 "$PKT/scripts/judge_il.py" "${t##*:}" "il-${t%%:*}.log" > "il-${t%%:*}.judge.tsv" || true
  done
  python3 "$PKT/scripts/hist_summary.py" hist > hist-summary.tsv
  python3 "$PKT/scripts/walks.py" suite-head.log suite-c4.log lawonly-head.log \
    lawonly-c4.log arm-*.leg.log probe-stdhist.log probe-tiehist.log \
    probe-tiealone.log probe-sp-std.log probe-sphi-std.log hist/*.log > walks.tsv
  # every W = 9 window (the window-fault probe, W = 2105, is judged by its
  # own expected failures, not here)
  python3 "$PKT/scripts/walk_audit.py" suite-*.log lawonly-*.log arm-*.leg.log \
    probe-stdhist.log probe-tiehist.log probe-tiealone.log probe-nodwell.log \
    probe-sp-std.log probe-sphi-std.log il-*.log hist/*.log wrap-*.log \
    crfonly-*.log lb-*.log > walk-audit.txt || true
  python3 "$PKT/scripts/standing_margins.py" walk-audit.txt > standing-margins.txt
  python3 "$PKT/scripts/compare_walks_table.py" "$EVID/author-r3/round3-boundary-walks.md" \
    lb-head.log lb-c4.log > walks-table-compare.txt || true ;;
*) echo "usage: $0 trees|launch1|probes|launch2|launch2b|launch3|analyse" >&2; exit 2 ;;
esac
