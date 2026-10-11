#!/usr/bin/env bash
# The one-guard probe (probe_forms.sh's m_*.sv files) through Vivado xvlog/xelab
# and synth_design -rtl, violating (P=1) and passing (P=0).
# Usage: vivado_probe_forms.sh <probe-dir>   (Vivado on PATH)
set -u; cd "$1" || exit 2
for f in m_*.sv; do
  w=xs_${f%.sv}; rm -rf $w; mkdir $w
  (cd $w && xvlog -sv ../$f > xvlog.log 2>&1) || { echo "== $f xvlog FAILED"; continue; }
  for p in 1 0; do
    out=$(cd $w && xelab -debug off -generic_top P=$p work.probe -s s$p 2>&1); rc=$?
    echo "== $f P=$p xelab rc=$rc :: $(grep -m1 -E '^(ERROR|WARNING|INFO): \[(VRFC|XSIM)' <<<"$out" | grep -E 'ERROR|WARNING|8279|4462|\$(fatal|error|warning|info)' )"
  done
done
{ echo "set_param general.maxThreads 4"
  for f in m_*.sv; do for p in 1 0; do
    echo "puts \"@@begin $f P=$p\""; echo "read_verilog -sv {$f}"
    echo "set rc [catch {synth_design -rtl -top probe -part xc7a100tfgg484-2 -generic P=$p}]"
    echo "catch {close_design}"; echo "remove_files [get_files]"; echo "puts \"@@end $f P=$p rc=\$rc\""; done; done; } > synth_probe.tcl
vivado -mode batch -nojournal -nolog -source synth_probe.tcl > synth_probe.log 2>&1
python3 - <<'PY'
import re
log = open("synth_probe.log").read()
for m in re.finditer(r"^@@begin (\S+ P=\d)\n(.*?)^@@end \S+ P=\d rc=(\d+)$", log, re.S | re.M):
    body = m.group(2)
    said = [l for l in body.splitlines() if re.match(r"^(ERROR|WARNING|CRITICAL WARNING|INFO): \[Synth 8-(6058|6157|6155|8277|7151|8293|6014)\]|^ERROR|\$(fatal|error|warning|info)", l)]
    print(f"== {m.group(1)} synth_design rc={m.group(3)} :: {(said[0] if said else '')[:200]}")
PY
