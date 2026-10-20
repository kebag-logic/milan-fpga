#!/usr/bin/env bash
# The labels the srp_top campaign grades on two suites keep one receipt (the
# later run). Repeat the earlier suite alone at the head, from a fresh export
# with the arm's patch, to record its failing words.
S=<scratch>
. $S/scripts/env.sh
H=$(cat $S/head.sha)
out=$S/rec/head-extra; mkdir -p $out
run() {
  local label=$1 suite=$2 group=$3 w=$S/extra/$1-$2
  rm -rf $w; mkdir -p $w
  git -C <lane> archive "$H" hdl tb/common tb/$suite tb/srp_top/mutations | tar -x -C $w
  (cd $w && git apply tb/srp_top/mutations/$label.patch) || { echo "apply failed" > $out/$label-$suite.log; return; }
  make -C $w/tb/$suite RUN_ARGS=$group > $out/$label-$suite.log 2>&1
  echo $? > $out/$label-$suite.rc
  rm -rf $w
}
run listener-settle-compare-dropped srp_top share
run listener-withdraw-ignores-riders srp_stream_fsms suite
run listener-teardown-keeps-declaring srp_stream_fsms suite
run listener-type-not-combined srp_stream_fsms suite
echo done > $out/ALL.done
