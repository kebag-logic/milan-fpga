#!/usr/bin/env bash
# stop_replay.sh <head> <set>: replay the job instances a set names, in order, one at a time, each on its own clean
# clone (ci_replay.py job), and print each job's own result from its result.json. docs: every docs.yml job a pull
# request runs; boundary: rtl-fast's changes, firmware-boundary and firmware-verilator
set -uo pipefail
H=$1; T=$MANAGEMENT/2026-09-23/665s7-a757b/tools
R=/data-2/milan/tmp/665s7-a757b/ci/${H:0:12}
case $2 in
  docs) jobs="docs:wire-accountability docs:docs-check-no-git docs:docs-gates-0 docs:docs-gates-1 docs:docs-gates-2 docs:docs-check docs:ci-fail-fast docs:ci-manifest docs:ci-cancel-tail" ;;
  boundary) jobs="rtl-fast:changes rtl-fast:firmware-boundary rtl-fast:firmware-verilator" ;;
esac
for j in $jobs; do
  IFS=: read -r wf job <<< "$j"
  python3 $T/ci_replay.py job "$H" "$wf" "$job" > "$R/$wf-$job.driver.log" 2>&1
  rc=$?
  verdict=$(python3 -c "import json,sys; print(json.load(open(sys.argv[1]))['result'])" "$R/jobs/${wf}__${job}/result.json" 2>&1)
  echo "$(date +%T) $wf/$job driver rc=$rc result=$verdict"
done
echo "$(date +%T) stop_replay.sh $2 done"
