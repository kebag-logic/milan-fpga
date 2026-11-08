#!/bin/sh
# usage: run_reviewer_scripts.sh CLONE WORK OUT
# Runs both round 3 reviewers' published scripts, unchanged, against the clone's HEAD and collects their output.
set -u
C=$1; W=$2; O=$3
R3=<reviews>/tsn26-r793-3/scripts
R4=<reviews>/tsn26-r794-3/scripts
export TOOLS=<tools>
export TMPDIR=<scratch>/tmp
rm -rf "$W"; mkdir -p "$W" "$O"
(cd "$C" && git rev-parse HEAD) > "$O/head.txt"
sh "$R3/run_reviewer_plants.sh" "$C" "$W/r793-plants" > "$O/r793-reviewer-plants.txt" 2>&1; echo "rc $?" >> "$O/r793-reviewer-plants.txt"
cp "$W/r793-plants/reviewer-plants.json" "$O/r793-reviewer-plants.json"
sh "$R3/run_probe.sh" "$C" "$W/r793-probe-r3" HEAD "$R3/probe_r3.cpp" 'TimerProbesAgainstTheDeferredBind.*:AcmpOwed.R3Probe*' > "$O/r793-probe-r3.txt" 2>&1; echo "rc $?" >> "$O/r793-probe-r3.txt"
sh "$R3/run_probe.sh" "$C" "$W/r793-refused" HEAD "$R3/probe_intermittent.cpp" 'AcmpOwed.R3ProbeRefusedPollKeepsTheHold' > "$O/r793-refused-poll.txt" 2>&1; echo "rc $?" >> "$O/r793-refused-poll.txt"
sh "$R3/run_probe_timer_ahead.sh" "$C" "$W/r793-timer-ahead" HEAD > "$O/r793-probe-timer-ahead.txt" 2>&1; echo "rc $?" >> "$O/r793-probe-timer-ahead.txt"
mkdir -p "$W/tree"; (cd "$C" && git archive HEAD) | tar -x -C "$W/tree"
bash "$R4/run_probes2.sh" "$W/tree" "$W/r794-p2" "$O/r794-probe2.txt"
bash "$R4/run_probes3.sh" "$W/tree" "$W/r794-p3" "$O/r794-probe3-boundary-head.txt" "$R4/probe_owed3.inc" 'AcmpOwedProbe3.*'
for p in reviewer-bind-wait-at-full reviewer-hold-every-timer reviewer-hold-second-no-resp; do
  bash "$R4/run_probes3.sh" "$W/tree" "$W/r794-p3-$p" "$O/r794-probe3-boundary-$p.txt" "$R4/probe_owed3.inc" 'AcmpOwedProbe3.*' "$p" "$R4/plants-r3.json"
done
bash "$R4/run_probes3.sh" "$W/tree" "$W/r794-p4" "$O/r794-probe4-gated-port.txt" "$R4/probe_owed4.inc" 'AcmpOwedProbe4.*'
bash "$R4/run_probes3.sh" "$W/tree" "$W/r794-p5" "$O/r794-probe5-kept-behind.txt" "$R4/probe_owed5.inc" 'AcmpOwedProbe5.*'
python3 -I "$R4/escape_check.py" "$W/tree" "$W/r794-escape" "$O/r794-escape-check.txt" "$R4/plants-r3.json"; echo "rc $?" >> "$O/r794-escape-check.txt"
for p in reviewer-bind-wait-at-full reviewer-hold-every-timer reviewer-hold-second-no-resp; do
  bash "$R4/plant_full.sh" "$W/tree" "$W/r794-full-$p" "$O/r794-full-suite-$p.txt" "$p" "$R4/plants-r3.json" 8
done
echo done > "$O/done"
