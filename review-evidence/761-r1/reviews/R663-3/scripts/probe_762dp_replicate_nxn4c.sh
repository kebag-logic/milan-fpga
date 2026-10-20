#!/usr/bin/env bash
# Reviewer probe (disposable): does [762-DP] grade the stopped_i bits above
# input 0? Plant stopped_i = {N_STREAMS{acmpl_stopped_v_w[0]}} (input 0's level
# replicated to every AAF input) in a byte copy of the head, build the obj_nxn4c
# leg through its own recipe and run it.
# Usage: probe_762dp_replicate_nxn4c.sh <copied-tree> <log-dir> <verilator>
set -u
T=$1; LOGS=$2; VL=$3
LEG=$T/tb/verilator/milan_dp
DP=$T/hdl/milan/milan_datapath.sv
mkdir -p "$LOGS"
ORIG='    .stopped_i      (acmpl_stopped_v_w[N_STREAMS-1:0]),'
MUT='    .stopped_i      ({N_STREAMS{acmpl_stopped_v_w[0]}}),'
cp "$DP" "$LOGS/dp.orig"
python3 -I - "$DP" "$ORIG" "$MUT" <<'PY'
import sys, pathlib
p = pathlib.Path(sys.argv[1]); s = p.read_text()
assert s.count(sys.argv[2] + "\n") == 1
p.write_text(s.replace(sys.argv[2] + "\n", sys.argv[3] + "\n"))
PY
diff -u "$LOGS/dp.orig" "$DP" | sed "s#$T#<tree>#g; s#$LOGS#<logs>#g" > "$LOGS/replicate.diff"
rm -f "$LOGS/dp.orig"
make -C "$LEG" VERILATOR="$VL" VERILATOR_JOBS=16 build-nxn4c > "$LOGS/replicate.build.raw.log" 2>&1
echo $? > "$LOGS/replicate.build.rc"
(cd "$LEG" && timeout 1500 ./obj_nxn4c/Vmilan_dp_nxn4c) > "$LOGS/replicate.run.log" 2>&1
echo $? > "$LOGS/replicate.run.rc"
grep -F '[FAIL]' "$LOGS/replicate.run.log" > "$LOGS/replicate.failures.txt"
grep -F '[762-DP]' "$LOGS/replicate.run.log" > "$LOGS/replicate.762dp.txt"
echo "replicate build_rc=$(cat $LOGS/replicate.build.rc) run_rc=$(cat $LOGS/replicate.run.rc) fails=$(wc -l < $LOGS/replicate.failures.txt) 762dp_lines=$(wc -l < $LOGS/replicate.762dp.txt) $(grep -E '^checks:' $LOGS/replicate.run.log)"
