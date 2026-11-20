#!/bin/bash
# analyse6.sh REV: the full re-measure's verdicts at each point from r6meas/REV (analyse.sh with its paths moved): the statement survey
# (survey_point4.py over every leg: the records', events', polls' and items' statements, the long notice, the datapath
# events) and the AECP records by class (the tree's record_classes.py), each into r4meas/out/.
set -u
T=<scratch>; . $T/bin/env.sh
REV=$1; M=$T/r6meas/$REV; O=$T/r6meas/out/$REV; mkdir -p $O
declare -A SP=([1x1]=1x1/1if [8x8-1if]=8x8/1if [8x8]=8x8/2if) NIF=([1x1]=1 [8x8-1if]=1 [8x8]=2)
for P in ${POINTS:-1x1 8x8-1if 8x8}; do
  C=${CLONES:-$T/clones/r6-meas-$REV}-$P; V=$M/views-$P; rm -rf $V; mkdir -p $V; parts=()
  for d in $M/$P/*/part*; do
    [ -f $d/results.json ] || continue
    a=$(basename $(dirname $d)); k=$(basename $d); parts+=($d)
    mkdir -p $V/$a-$k; ln -s $d $V/$a-$k/results; ln -s $M/$P/$a/build.json $V/$a-$k/build.json
  done
  SURVEY_POINT=${SP[$P]} SURVEY_NIF=${NIF[$P]} python3 -I $T/r4meas/survey_point4.py $C $T/tools/survey $O/survey-$P $V/* > $O/survey-$P.out 2>&1
  echo "survey $P rc=$?" | tee $O/survey-$P.rc
  python3 -I $C/tb/verilator/ctrl_service_budget/record_classes.py "${parts[@]}" > $O/record-classes-$P.txt 2>&1
  echo "record_classes $P rc=$?" | tee $O/record-classes-$P.rc
  for f in $M/$P/*.part*.log; do echo "$(basename $f): $(grep -h 'groups graded' $f | tail -1)"; done > $O/parts-$P.txt
  grep -h -E '^(BUDGET|STATED|REFUSED|NOTICE|SAVE|AGED)' $M/$P/*.part*.log | cut -c1-240 > $O/findings-$P.txt
done
