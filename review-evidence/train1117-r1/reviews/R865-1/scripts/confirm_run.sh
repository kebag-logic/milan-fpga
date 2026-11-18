#!/bin/bash
# Run the named groups on an existing build (run.py --reuse-build, the formal options); print each log's sha256.
# usage: confirm_run.sh <clone> <build dir> <point> <arm> <groups>
c=$1; b=$2; pt=$3; arm=$4; groups=$5
rm -rf "$b/part0"
python3 -B "$c/tb/verilator/ctrl_service_budget/run.py" --point "$pt" --build-dir "$b" --reuse-build --out "$b/part0" \
  --groups "$groups" --record-budget-findings --record-share-findings --jobs 2 --variant "$arm"
rc=$?
for g in ${groups//,/ }; do echo "LOG $g $(sha256sum "$b/part0/$g.log" | cut -c1-64)"; done
exit $rc
