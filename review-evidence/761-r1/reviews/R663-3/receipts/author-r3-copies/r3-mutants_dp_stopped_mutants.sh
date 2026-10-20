#!/usr/bin/env bash
# Plant each stopped_i wiring mutant in milan_datapath.sv of a disposable clean
# clone, rebuild the obj_nxn4c leg (the shipping Arty 4x4 shape) through the
# Makefile's own recipe, run it, and keep its log; then restore the file and
# run the clean leg as the positive control. Each leg runs from its own
# directory, where it reads ucode.hex and ltn_rom.hex. Usage:
#   dp_stopped_mutants.sh <clone> <log-dir>
# Exit 0 only if every mutant leg fails at least one [762-DP] check and the
# clean leg passes.
set -u
CLONE=$1; LOGS=$2
DP=$CLONE/hdl/milan/milan_datapath.sv
LEG=$CLONE/tb/verilator/milan_dp
ORIG='    .stopped_i      (acmpl_stopped_v_w[N_STREAMS-1:0]),'
declare -A MUT=(
  [tie0]="    .stopped_i      ('0),"
  [sink1]='    .stopped_i      (acmpl_stopped_v_w[N_STREAMS:1]),'
  [bound]='    .stopped_i      (acmpl_bound_v_w[N_STREAMS-1:0]),'
)
mkdir -p "$LOGS"
[ "$(grep -cxF -- "$ORIG" "$DP")" = 1 ] || { echo "anchor not unique"; exit 2; }
cp "$DP" "$LOGS/milan_datapath.sv.orig"
worst=0
for m in tie0 sink1 bound; do
  python3 - "$DP" "$ORIG" "${MUT[$m]}" <<'PY'
import sys, pathlib
p = pathlib.Path(sys.argv[1]); s = p.read_text()
assert s.count(sys.argv[2] + "\n") == 1
p.write_text(s.replace(sys.argv[2] + "\n", sys.argv[3] + "\n"))
PY
  diff -u "$LOGS/milan_datapath.sv.orig" "$DP" | sed "s#$CLONE#<clone>#g" > "$LOGS/$m.diff"
  make -C "$LEG" build-nxn4c > "$LOGS/$m.build.log" 2>&1; brc=$?
  (cd "$LEG" && ./obj_nxn4c/Vmilan_dp_nxn4c) > "$LOGS/$m.run.log" 2>&1; rrc=$?
  cp "$LOGS/milan_datapath.sv.orig" "$DP"
  grep -F '[FAIL]' "$LOGS/$m.run.log" > "$LOGS/$m.failures.txt"
  n762=$(grep -cF '[762-DP]' "$LOGS/$m.failures.txt")
  nall=$(wc -l < "$LOGS/$m.failures.txt")
  echo "$m build_rc=$brc run_rc=$rrc failing_checks=$nall of_which_762DP=$n762"
  if [ $brc -ne 0 ] || [ $rrc -eq 0 ] || [ "$n762" -eq 0 ]; then worst=1; fi
done
make -C "$LEG" build-nxn4c > "$LOGS/clean.build.log" 2>&1; brc=$?
(cd "$LEG" && ./obj_nxn4c/Vmilan_dp_nxn4c) > "$LOGS/clean.run.log" 2>&1; rrc=$?
echo "clean build_rc=$brc run_rc=$rrc $(tail -2 "$LOGS/clean.run.log" | head -1)"
if [ $brc -ne 0 ] || [ $rrc -ne 0 ]; then worst=1; fi
rm -f "$LOGS/milan_datapath.sv.orig"
exit $worst
