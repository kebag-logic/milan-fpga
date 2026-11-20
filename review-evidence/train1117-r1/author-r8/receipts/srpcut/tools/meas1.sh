#!/bin/bash
# meas1.sh CLONE BUILD OUT: 8x8/1if's valid-destinations srp-talker-held on BUILD (legs.py build), once (the harness
# is deterministic, round 5's attribution), read by the full re-measure's survey (survey_point4.py). Scratch only.
set -u
T=<scratch>; . $T/bin/env.sh
C=$1 B=$2 O=$3; mkdir -p $O
echo "HEAD $(git -C $C rev-parse --short=8 HEAD) dirty $(git -C $C status --porcelain | wc -l) start $(date +%T)"
python3 -B $C/tb/verilator/ctrl_service_budget/run.py --point 8x8-1if --build-dir $B --reuse-build --out $O/results \
  --groups srp-talker-held --variant valid-destinations --record-budget-findings --record-share-findings --jobs 1 > $O/run.log 2>&1
echo "run rc=$? $(date +%T)"; ln -sf $B/build.json $O/build.json
SURVEY_POINT=8x8/1if SURVEY_NIF=1 python3 -I $T/r4meas/survey_point4.py $C $T/tools/survey $O/survey $O > $O/survey.out 2>&1
echo "survey rc=$?"; cat $O/survey.out | head -12; grep -E "record.srp|item.reclaim |item.record |base " $O/survey/ordinary-costs/costs.txt
echo "END $(date +%T)"
