#!/bin/bash
# Review R489-1 campaign driver. Starts every independent job detached, each
# with its own log and rc file under $P/receipts; poll with wait_rc.sh.
# Usage: run_all.sh <packet-dir> <stage: 1|2>
#   stage 1: head and base full srp_top suites, the PR's mutant campaign
#            (--only the two new arms, which also runs their control), and the
#            reviewer probes built by make_probes.py (lvleave group only)
#   stage 2: the base full srp_top suite with each new mutant planted
#            (trees prepared with git archive + git apply, see REPORT.md)
set -u
P=$1; STAGE=$2
S=$P/scratch
R=$P/receipts
export VERILATOR=$P/scripts/vl-wrap.sh VL_J=${VL_J:-3}
export TMPDIR=$S/tmp
mkdir -p "$R" "$TMPDIR"

launch() {  # name, dir, command...
  local name=$1 dir=$2; shift 2
  rm -f "$R/$name.rc"
  ( cd "$dir" && "$@" ) > "$R/$name.log" 2>&1 < /dev/null; echo $? > "$R/$name.rc"
}
export -f launch
export R

if [ "$STAGE" = 1 ]; then
  setsid nohup bash -c 'launch srp_top-full-head '"$S"'/head make -C tb/srp_top' >/dev/null 2>&1 &
  setsid nohup bash -c 'launch srp_top-full-base '"$S"'/base make -C tb/srp_top' >/dev/null 2>&1 &
  setsid nohup bash -c 'launch mutants-head '"$S"'/head python3 tb/srp_top/mutants.py --only lv-second-lv-ends,lv-never-ends --jobs 3 --output '"$R"'/mutants-head' >/dev/null 2>&1 &
  setsid nohup bash -c '
  for pair in "trace lv-restarts-timer" "lv-in-lv-ends-now leave-5002" "leave-4998 own-la-no-age" "peer-la-no-age harness-no-lv"; do
    for n in $pair; do launch probe-$n '"$S"'/probe-$n make -C tb/srp_top RUN_ARGS=lvleave & done
    wait
  done
  echo 0 > '"$R"'/probes-done.rc' >/dev/null 2>&1 &
fi
if [ "$STAGE" = 2 ]; then
  for m in lv-second-lv-ends lv-never-ends; do
    setsid nohup bash -c 'launch srp_top-full-base-planted-'"$m"' '"$S"'/base-'"$m"' make -C tb/srp_top' >/dev/null 2>&1 &
  done
fi
echo "stage $STAGE launched"
