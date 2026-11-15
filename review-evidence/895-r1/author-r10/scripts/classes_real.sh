#!/bin/bash
# classes_real.sh TREE OUT: the head's record class grader (record_classes.py, the real-leg CLI) over every preserved
# leg of rounds 8 and 9 at both points, one pass (1x1/1if: arm A merged, answering-every-port, valid-destinations,
# answering-ports; 8x8/2if: the same, valid-destinations rerun in round 9), then the corrected survey
# (round10/scripts/costs_vs_stated.py) at each point over the same legs and round 8's parser costs. Read-only on TREE
# and on the legs. Logs and rcs in OUT.
set -u
T=$1 O=$2
B=/data-2/milan/tmp/895-a775/builds
C=/data-2/milan/tmp/895-a775/r8
S10=$MANAGEMENT/2026-09-23/895-a775/round10/scripts
mkdir -p "$O"
cd "$T/tb/verilator/ctrl_service_budget" || exit 3
echo "tree $(git -C "$T" rev-parse HEAD) dirty $(git -C "$T" status --porcelain | wc -l)" > "$O/HEAD.txt"
L1=("$B/R8-A1-view/results" "$B/R8-N1/results" "$B/R8-W1/results" "$B/R8-B1/results")
L8=("$B/R8-A8-view/results" "$B/R8-N8/results" "$B/R9-W8/results" "$B/R8-B8/results")
python3 -I -B record_classes.py "${L1[@]}" "${L8[@]}" > "$O/record_classes-real.log" 2>&1
echo $? > "$O/record_classes-real.rc"
python3 -I -B "$S10/costs_vs_stated.py" "$T" 1x1/1if "$C/costs-1x1" A="${L1[0]}" N="${L1[1]}" W="${L1[2]}" \
  B="${L1[3]}" > "$O/survey-1x1.txt" 2>&1
echo $? > "$O/survey-1x1.rc"
python3 -I -B "$S10/costs_vs_stated.py" "$T" 8x8/2if "$C/costs-8x8" A="${L8[0]}" N="${L8[1]}" W="${L8[2]}" \
  B="${L8[3]}" > "$O/survey-8x8.txt" 2>&1
echo $? > "$O/survey-8x8.rc"
