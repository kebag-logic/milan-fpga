#!/usr/bin/env bash
# F1 probes at a scratch parent tree (1269cdaf + c8 + p2 + amended c10, the
# protocol-processor submodule at the head under review). Each probe mutates
# one file, runs gate 3 (check_rtl_source_lists.py) or its --selftest, records
# rc and the verdict lines, and restores the file from a saved copy.
# usage: parent_f1_probes.sh <parent-tree> <out-dir>
set -uo pipefail
T=$1 OUT=$2; mkdir -p "$OUT"; cd "$T" || exit 2
G=scripts/check_rtl_source_lists.py
# pristine copies of the three files the probes mutate, restored after each
BK=$(mktemp -d); trap 'rm -rf "$BK"' EXIT
cp -p $G "$BK/gate.py"; cp -p scripts/processor_yosys_tops.budget "$BK/budget"
cp -p protocol-processor/syn/yosys/run.sh "$BK/run.sh"
probe() { # $1 = name, $2 = mode (gate|selftest), $3 = python mutation (exec'd in $T)
  local name=$1 mode=$2 code=$3 rc
  python3 -c "$code" || { echo "$name: mutation did not apply"; return; }
  if [ "$mode" = gate ]; then python3 $G >"$OUT/$name.log" 2>&1; else python3 $G --selftest >"$OUT/$name.log" 2>&1; fi
  rc=$?; echo "rc=$rc" >>"$OUT/$name.log"
  cp -p "$BK/gate.py" $G; cp -p "$BK/budget" scripts/processor_yosys_tops.budget
  cp -p "$BK/run.sh" protocol-processor/syn/yosys/run.sh
  printf '%-34s %-8s rc=%s  %s\n' "$name" "$mode" "$rc" \
    "$(grep -E '^(STALE RECORD|TOPS DRIFT|RTL source-list gate|\[FAIL\])|checks:' "$OUT/$name.log" | cut -c1-140 | tr '\n' '|')"
}
R='import re,pathlib as p
def sub(f,a,b):
    t=p.Path(f).read_text(); assert t.count(a)==1,(f,a); p.Path(f).write_text(t.replace(a,b))
'
probe control-gate gate "$R"
probe control-selftest selftest "$R"
probe live-stale-record gate "$R
t=p.Path('scripts/processor_yosys_tops.budget'); t.write_text(t.read_text()+'KL_srp_top  r448 planted stale record\n')"
probe live-unrecorded-omission gate "$R
sub('protocol-processor/syn/yosys/run.sh','KL_srp_top protocol_processor_top)','protocol_processor_top)')"
probe live-recorded-omission gate "$R
sub('protocol-processor/syn/yosys/run.sh','KL_srp_top protocol_processor_top)','protocol_processor_top)')
t=p.Path('scripts/processor_yosys_tops.budget'); t.write_text(t.read_text()+'KL_srp_top  r448 recorded omission\n')"
probe mut-verdict-drops-stale selftest "$R
sub('$G','        for name in stale:\n            findings += 1\n            lines.append(f\"STALE RECORD','        for name in []:\n            findings += 1\n            lines.append(f\"STALE RECORD')"
probe mut-verdict-drops-drift selftest "$R
sub('$G','        for name in unrecorded:\n            findings += 1\n            lines.append(f\"TOPS DRIFT','        for name in []:\n            findings += 1\n            lines.append(f\"TOPS DRIFT')"
probe mut-stale-not-counted selftest "$R
sub('$G','        for name in stale:\n            findings += 1\n','        for name in stale:\n            findings += 0\n')"
probe mut-drift-not-counted selftest "$R
sub('$G','        for name in unrecorded:\n            findings += 1\n','        for name in unrecorded:\n            findings += 0\n')"
probe mut-compare-no-stale selftest "$R
sub('$G','    stale = sorted(n for n in recorded if n not in missing)','    stale = []')"
probe mut-compare-no-unrecorded selftest "$R
sub('$G','    unrecorded = sorted(missing - set(recorded))','    unrecorded = []')"
