#!/bin/sh
# R488-2 reviewer runs, in the order they were made. Every tree is a
# `git archive` export under $PKT/scratch; the review clone is never written.
# usage: run_review.sh REPO   (PKT = this script's packet; put a Verilator 5.050
# `verilator` in $PKT/bin first). Launch with launch.sh, collect with wait.sh.
set -u
R=$1
PKT=${PKT:-$(cd "$(dirname "$0")/.." && pwd)}; export PKT
S=$PKT/scratch; L=$PKT/scripts/launch.sh
HEAD=9050c4bbd25556929a0f24fb98258bc98e3bcfbe
PRE=21c6f7096ac80007f723de59c6f717f55bd34cfc     # merged main, pre-fix RTL
BASE=ead8036035affd53ef4b29979190f2f4f67084c0
x() { rm -rf "$S/$1"; mkdir -p "$S/$1"; (cd "$R" && git archive "$2") | tar -x -C "$S/$1"; }

# wave 1: head suites and the full SRP campaign
x w_srptop $HEAD; $L head-srp_top "$S/w_srptop/tb/srp_top" make
x w_fsms $HEAD;   $L head-srp_stream_fsms "$S/w_fsms/tb/srp_stream_fsms" make
x w_camp $HEAD;   $L srp-campaign "$S/w_camp" python3 tb/srp_top/mutants.py --output "$S/camp_out" --jobs 6
# reviewer probe: a JoinIn swept across the expiry clock (group r488join)
x w_pj $HEAD; python3 "$PKT/scripts/probe_join_collision.py" "$S/w_pj"
$L probe-join-collision "$S/w_pj/tb/srp_top" make run RUN_ARGS=r488join
"$PKT/scripts/wait.sh" head-srp_top head-srp_stream_fsms srp-campaign probe-join-collision

# reviewer faults, each through SC1, the lvcoll sweep and the r488join probe
for F in listener-only-restore talker-only-restore expiry-over-renewal; do
  for r in fsms lvcoll join; do
    x m-$F-$r $HEAD; python3 "$PKT/scripts/probe_join_collision.py" "$S/m-$F-$r" >/dev/null
    python3 "$PKT/scripts/reviewer_mutants.py" "$R" "$S/m-$F-$r" $F > "$PKT/receipts/fault-$F.diff"
  done
  $L fault-$F-fsms "$S/m-$F-fsms/tb/srp_stream_fsms" make run
  $L fault-$F-lvcoll "$S/m-$F-lvcoll/tb/srp_top" make run RUN_ARGS=lvcoll
  $L fault-$F-join "$S/m-$F-join/tb/srp_top" make run RUN_ARGS=r488join
done
# the README's checked-in arms, through the complete head suite or their group
x m-lv-never-ends-full $HEAD
python3 "$PKT/scripts/reviewer_mutants.py" "$R" "$S/m-lv-never-ends-full" lv-never-ends > "$PKT/receipts/fault-lv-never-ends.diff"
$L fault-lv-never-ends-full "$S/m-lv-never-ends-full/tb/srp_top" make
for m in lv-second-lv-ends:full talker-strict-lv:lvleave talker-no-expiry:lvleave lv-expiry-dropped:lvcoll; do
  l=${m%%:*}; g=${m##*:}; x c-$l-$g $HEAD
  (cd "$S/c-$l-$g" && git apply "$R/tb/srp_top/mutations/$l.patch")
  if [ $g = full ]; then $L patch-$l-$g "$S/c-$l-$g/tb/srp_top" make
  else $L patch-$l-$g "$S/c-$l-$g/tb/srp_top" make run RUN_ARGS=$g; fi
done

# base counts for the bank arithmetic (PRE with the head's D3 format fix for pp_top)
for rev in $PRE $BASE; do
  t=base-$(echo $rev | cut -c1-8); x $t $rev
  $L $t-srp_top "$S/$t/tb/srp_top" make
  $L $t-srp_stream_fsms "$S/$t/tb/srp_stream_fsms" make
done
(cd "$R" && git diff $PRE $HEAD -- tb/pp_top/d3_phases.hpp) > "$S/d3fix.patch"
(cd "$S/base-21c6f709" && git apply "$S/d3fix.patch")
$L base-21c6f709fix-pp_top "$S/base-21c6f709/tb/pp_top" make
$L base-21c6f709-timer_map "$S/base-21c6f709/tb/timer_map" make
x w_pp $HEAD
$L head-pp_top "$S/w_pp/tb/pp_top" make
$L head-timer_map "$S/w_pp/tb/timer_map" make

# R489-1-S1 recheck: group S with both Lvs removed from its stimulus (see REPORT)
# static gates in a scratch clone: make check, lint, matrix (foreground)
# integrity: clone_integrity.sh "$R" $HEAD 3bcc8532549ea69139323a863049022d10f799c1
