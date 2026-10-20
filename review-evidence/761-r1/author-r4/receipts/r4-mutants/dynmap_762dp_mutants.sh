#!/usr/bin/env bash
# The stopped_i wiring mutants on the obj_dynmap leg: endstation_ax7101_1x1_tdm8,
# the shipping AX7101 1x1 TDM8 geometry (N_STREAMS=1, 8 wire channels, TDM8
# master, loopback lane, I2S playback and render LPF pruned; the obj_ax1x1
# verification substitutes: gPTP option OFF, 100 MHz fabric clock, render lane
# pruned). At N_STREAMS=1 the CRF Media Clock Input is ACMP sink 1, so the
# sink1 form feeds AAF input 0 the CRF sink's stopped level.
#
# Each mutant is a copy of milan_datapath.sv with the one stopped_i line
# replaced, built through the Makefile's own dynmap-build recipe with DP_SRC
# and DYNMAP_MDIR overridden (the dynmap_mutants.py route), so the clone's
# tracked files are never edited. Each binary runs from the leg directory,
# where it reads ucode.hex and ltn_rom.hex. The clean leg is built and run the
# same way as the positive control.
#
# Usage: dynmap_762dp_mutants.sh <clone> <work-dir> <log-dir>
# Exit 0 only if every build succeeds, each mutant fails EXACTLY its expected
# [762-DP] checks and nothing else, and the clean leg passes with no failure.
set -u
CLONE=$1; WORK=$2; LOGS=$3
DP=$CLONE/hdl/milan/milan_datapath.sv
LEG=$CLONE/tb/verilator/milan_dp
ORIG='    .stopped_i      (acmpl_stopped_v_w[N_STREAMS-1:0]),'
declare -A MUT=(
  [tie0]="    .stopped_i      ('0),"
  [sink1]='    .stopped_i      (acmpl_stopped_v_w[N_STREAMS:1]),'
  [bound]='    .stopped_i      (acmpl_bound_v_w[N_STREAMS-1:0]),'
)
GAP0='[762-DP] 2 stopped gap: STREAM_INTERRUPTED +0'
SIL0='[762-DP] 3 stopped silence: STREAM_INTERRUPTED +0'
GAP1='[762-DP] 4 started gap: STREAM_INTERRUPTED +1'
declare -A WANT=(
  [tie0]="$GAP0"$'\n'"$SIL0"
  [sink1]="$GAP0"$'\n'"$SIL0"
  [bound]="$GAP1"
)
mkdir -p "$WORK" "$LOGS"
[ "$(grep -cxF -- "$ORIG" "$DP")" = 1 ] || { echo "anchor not unique"; exit 2; }
# REDACT_TOOLS and REDACT_DATA name the host's toolchain and data roots, so
# that the published logs carry placeholders and this file carries no host path.
redact() { sed -e "s#$CLONE#<clone>#g" -e "s#$WORK#<work>#g" -e "s#${REDACT_TOOLS:-<tools>}#<tools>#g" \
               -e "s#${REDACT_DATA:-<data>}#<data>#g" -e "s#$HOME#\$HOME#g"; }
names() { grep -F '[FAIL]' "$1" | sed -E 's/^ *\[FAIL\] +//; s/ +(=|got|expected).*$//' | sort; }
worst=0
for m in tie0 sink1 bound clean; do
  src=$DP
  if [ "$m" != clean ]; then
    src=$WORK/$m.milan_datapath.sv
    python3 - "$DP" "$src" "$ORIG" "${MUT[$m]}" <<'PY'
import sys, pathlib
s = pathlib.Path(sys.argv[1]).read_text()
assert s.count(sys.argv[3] + "\n") == 1
pathlib.Path(sys.argv[2]).write_text(s.replace(sys.argv[3] + "\n", sys.argv[4] + "\n"))
PY
    diff -u "$DP" "$src" | redact > "$LOGS/$m.diff"
  fi
  make -C "$LEG" dynmap-build DP_SRC="$src" DYNMAP_MDIR="$WORK/obj_$m" > "$WORK/$m.build.log" 2>&1; brc=$?
  (cd "$LEG" && "$WORK/obj_$m/Vmilan_dp_dynmap") > "$WORK/$m.run.log" 2>&1; rrc=$?
  redact < "$WORK/$m.build.log" > "$LOGS/$m.build.log"
  redact < "$WORK/$m.run.log" > "$LOGS/$m.run.log"
  grep -F '[FAIL]' "$LOGS/$m.run.log" > "$LOGS/$m.failures.txt"
  got=$(names "$LOGS/$m.run.log")
  tally=$(grep -E '^checks: ' "$LOGS/$m.run.log" | tail -1)
  n762=$(grep -c '\[762-DP\] ' "$LOGS/$m.run.log")
  if [ "$m" = clean ]; then
    ok=$([ $brc -eq 0 ] && [ $rrc -eq 0 ] && [ -z "$got" ] && echo 1 || echo 0)
  else
    want=$(printf '%s\n' "${WANT[$m]}" | sort)
    ok=$([ $brc -eq 0 ] && [ $rrc -ne 0 ] && [ "$got" = "$want" ] && echo 1 || echo 0)
  fi
  echo "$m build_rc=$brc run_rc=$rrc [762-DP]_lines=$n762 $tally exact_expected=$ok"
  [ "$ok" = 1 ] || worst=1
done
exit $worst
