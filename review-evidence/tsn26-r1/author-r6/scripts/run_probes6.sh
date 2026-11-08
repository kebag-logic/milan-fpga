#!/bin/sh
# usage: run_probes6.sh CLONE WORK OUT
# Runs both reviewers' round 4 and round 5 probes, unchanged, against the clone's HEAD. The internal review's
# runners export the clone's commit (git archive); the external review's runner copies a git archive of it.
# The clone is never written. Each probe's full output and rc go to OUT; OUT/done is written last.
set -u
C=$1; W=$2; O=$3
R=<reviews>
I5=$R/tsn26-r793-5/scripts
E5=$R/tsn26-r794-5/scripts
export TOOLS=<tools>
export TMPDIR=<scratch>/tmp
rm -rf "$W" "$O"; mkdir -p "$W" "$O"
(cd "$C" && git rev-parse HEAD) > "$O/head.txt"
sha256sum "$I5"/probe_r3.cpp "$I5"/probe_intermittent.cpp "$I5"/probe_timer_ahead.cpp "$I5"/probe_r4.cpp \
  "$I5"/probe_r4b.cpp "$I5"/probe_r4c.cpp "$I5"/probe_r5.cpp "$I5"/probe_r5b.cpp "$I5"/run_probe_j4.sh \
  "$I5"/run_probe_timer_ahead.sh "$I5"/plant_escape.sh "$I5"/env.sh "$E5"/probe_owed6.inc "$E5"/probe_owed7.inc \
  "$E5"/run_probes3.sh "$E5"/apply_plant.py "$E5"/escape_check5.py "$E5"/plants-r5.json > "$O/inputs.sha256"
cat "$I5/probe_r3.cpp" "$I5/probe_intermittent.cpp" > "$W/probe_r3_intermittent.cpp"
cat "$I5/probe_r4.cpp" "$I5/probe_r4b.cpp" > "$W/probe_r4_r4b.cpp"
sha256sum "$W/probe_r3_intermittent.cpp" "$W/probe_r4_r4b.cpp" >> "$O/inputs.sha256"
pr() { sh "$I5/run_probe_j4.sh" "$C" "$W/$1" HEAD "$2" "$3" > "$O/$1.txt" 2>&1; echo "rc $?" >> "$O/$1.txt"; }
pr r3-head "$W/probe_r3_intermittent.cpp" 'TimerProbesAgainstTheDeferredBind.*:AcmpOwed.R3Probe*'
sh "$I5/run_probe_timer_ahead.sh" "$C" "$W/timer-ahead-head" HEAD > "$O/timer-ahead-head.txt" 2>&1; echo "rc $?" >> "$O/timer-ahead-head.txt"
pr r4-head "$W/probe_r4_r4b.cpp" 'AcmpOwed.R4ProbeOneFramePerAcceptedPoll:AcmpOwed.R4ProbeBudgetForAPortThatOffersOneFramePerPoll'
pr r4c-head "$I5/probe_r4c.cpp" 'AcmpOwed.R4ProbeHeldProbeBoundAndCancel'
pr r5-head "$I5/probe_r5.cpp" 'AcmpOwed.R5ProbeLongHeldWait'
pr r5b-head "$I5/probe_r5b.cpp" 'AcmpOwed.R5ProbeLongHeldWaitWithOneGap'
for pair in owed-held-probe-owed-at-the-poll:CommandOfferedAfterTheTakenBindDelaysTheHeldRetry \
    owed-bind-wait-only-on-a-second-decline:KeptCommandsBehindSevenOwedLeaveOnePassSooner \
    owed-answer-keeps-the-hold:AnsweredProbeEndsTheHoldOfItsRetry; do
  p=${pair%%:*}; t=AcmpOwed.${pair#*:}
  sh "$I5/plant_escape.sh" "$C" "$W/escape-$p" HEAD "$p" "$t" > "$O/internal-plant-escape-$p.txt" 2>&1
  echo "rc $?" >> "$O/internal-plant-escape-$p.txt"
done
mkdir -p "$W/tree"; (cd "$C" && git archive HEAD) | tar -x -C "$W/tree"
bash "$E5/run_probes3.sh" "$W/tree" "$W/p6" "$O/probe6-head.txt" "$E5/probe_owed6.inc" 'AcmpOwedProbe6.*'
bash "$E5/run_probes3.sh" "$W/tree" "$W/p7" "$O/probe7-head.txt" "$E5/probe_owed7.inc" 'AcmpOwedProbe7.*'
python3 -I "$E5/escape_check5.py" "$W/tree" "$W/e5" "$O/escape-check5-head.txt" "$E5/plants-r5.json" > "$O/escape-check5-head.log" 2>&1
echo "rc $?" >> "$O/escape-check5-head.log"
echo done > "$O/done"
