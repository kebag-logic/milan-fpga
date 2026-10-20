#!/usr/bin/env bash
# Reviewer probe (disposable): run the [762-DP] integrated case on the shipping
# AX7101 1x1 TDM8 geometry (the dynmap recipe: SHAPE_AX1x1, 8 wire channels,
# TDM8 master, LOOPBACK_P=1, LPF_P=0), clean and with three planted mutants at
# milan_datapath.sv's avtp_rx_monitor .stopped_i connection.
# Usage: probe_762dp_ax1x1.sh <copied-tree> <log-dir> <verilator>
# The copied tree is a byte copy of the exact head with no .git; nothing in
# the reviewed clone is touched.
set -u
T=$1; LOGS=$2; VL=$3
LEG=$T/tb/verilator/milan_dp
DP=$T/hdl/milan/milan_datapath.sv
mkdir -p "$LOGS"
ORIG='    .stopped_i      (acmpl_stopped_v_w[N_STREAMS-1:0]),'
[ "$(grep -cxF -- "$ORIG" "$DP")" = 1 ] || { echo "anchor not unique"; exit 2; }
# 1. harness: in the dynmap leg's early-exit branch, run the TRAP-1 bind, the
#    5.3.8.7 discard section and [762-DP] instead of the dynmap section
python3 -I - "$LEG/sim_nxn.cpp" <<'PY'
import sys, pathlib
p = pathlib.Path(sys.argv[1]); s = p.read_text()
old = "        dynmap_power_on_and_adaptation_section();\n"
assert s.count(old) == 1
new = ("        { const unsigned long a0 = aprb_armed();\n"
       "          bind_listener_zero_over_acmp_with_an_explicit_sid();\n"
       "          grade_the_bound_alias_verdict(a0);\n"
       "          prove_a_stopped_stream_input_discards();\n"
       "          prove_a_stopped_stream_input_counts_no_interruption(); }\n")
p.write_text(s.replace(old, new))
PY
# 2. mutant datapath copies (DP_SRC override)
mkdir -p "$T/probe_dp"
declare -A MUT=(
  [clean]="$ORIG"
  [tie0]="    .stopped_i      ('0),"
  [sink1]='    .stopped_i      (acmpl_stopped_v_w[N_STREAMS:1]),'
  [bound]='    .stopped_i      (acmpl_bound_v_w[N_STREAMS-1:0]),'
)
for m in clean tie0 sink1 bound; do
  python3 -I - "$DP" "$T/probe_dp/$m.sv" "$ORIG" "${MUT[$m]}" <<'PY'
import sys, pathlib
s = pathlib.Path(sys.argv[1]).read_text()
assert s.count(sys.argv[3] + "\n") == 1
pathlib.Path(sys.argv[2]).write_text(s.replace(sys.argv[3] + "\n", sys.argv[4] + "\n"))
PY
  diff -u "$DP" "$T/probe_dp/$m.sv" | sed "s#$T#<tree>#g" > "$LOGS/$m.diff"
done
# 3. shared prerequisites once, then four builds in parallel
make -C "$LEG" VERILATOR="$VL" ltn_rom.hex ucode.hex > "$LOGS/prereq.log" 2>&1 || { echo prereq failed; exit 2; }
for m in clean tie0 sink1 bound; do
  ( make -C "$LEG" VERILATOR="$VL" VERILATOR_JOBS=4 DYNMAP_MDIR=obj_p762_$m \
      DP_SRC="$T/probe_dp/$m.sv" dynmap-build > "$LOGS/$m.build.log" 2>&1
    echo $? > "$LOGS/$m.build.rc"
    (cd "$LEG" && timeout 3000 ./obj_p762_$m/Vmilan_dp_dynmap) > "$LOGS/$m.run.log" 2>&1
    echo $? > "$LOGS/$m.run.rc" ) &
done
wait
for m in clean tie0 sink1 bound; do
  grep -F '[FAIL]' "$LOGS/$m.run.log" > "$LOGS/$m.failures.txt"
  grep -F '[762-DP]' "$LOGS/$m.run.log" > "$LOGS/$m.762dp.txt"
  echo "$m build_rc=$(cat $LOGS/$m.build.rc) run_rc=$(cat $LOGS/$m.run.rc) fails=$(wc -l < $LOGS/$m.failures.txt) fails_762DP=$(grep -cF '[762-DP]' $LOGS/$m.failures.txt) $(grep -E '^checks:' $LOGS/$m.run.log)"
done
