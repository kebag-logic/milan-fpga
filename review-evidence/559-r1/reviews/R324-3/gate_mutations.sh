#!/usr/bin/env bash
# R324-3: real-source mutations against scripts/check_nvm_capture.py.
# Each arm edits a scratch COPY of the exact-head clone, runs the gate, records
# rc and the first FAIL line, then restores the copy with git and proves it clean.
# Usage: CLONE=<exact-head clone> bash gate_mutations.sh > receipts/gate_mutations.log
set -uo pipefail
PKT=$(cd "$(dirname "$0")" && pwd)
: "${CLONE:?set CLONE to the exact-head review clone}"
R=$PKT/scratch/repo_mut
rm -rf "$R"; cp -a "$CLONE" "$R"; cd "$R"
M=tb/verilator/nvm_capture_cpu/measurements.json
arm() {  # name, expected rc, python edit program
  local name=$1 want=$2 prog=$3
  python3 - "$R" <<PY
import json, re, sys
from pathlib import Path
root = Path(sys.argv[1])
def sub(path, old, new, count=1):
    p = root / path; s = p.read_text()
    assert s.count(old) >= 1, (path, old)
    p.write_text(s.replace(old, new, count))
def receipt(fn):
    p = root / '$M'; r = json.loads(p.read_text()); fn(r); p.write_text(json.dumps(r, indent=2) + '\n')
$prog
PY
  out=$(python3 scripts/check_nvm_capture.py 2>&1); rc=$?
  verdict=$([ "$rc" = "$want" ] && echo EXPECTED || echo UNEXPECTED)
  echo "ARM $name rc=$rc want=$want $verdict :: $(printf '%s\n' "$out" | grep -m1 -E '^(FAIL|PASS)' | cut -c1-220)"
  git checkout -q -- . && git clean -qfd && [ -z "$(git status --porcelain)" ] || echo "RESTORE FAILED $name"
}
arm baseline 0 'pass'
arm yaml-8x8-cpu-clock-50MHz 1 'sub("configs/endstation_ax7101_8x8.yaml", "milan_clk_hz: 100000000", "milan_clk_hz: 50000000 ")'
arm yaml-1x1-cpu-clock 1 'sub("configs/endstation_ax7101_1x1_tdm8.yaml", "milan_clk_hz: 50000000", "milan_clk_hz: 62500000")'
arm yaml-8x8-sys-clock 1 'sub("configs/endstation_ax7101_8x8.yaml", "sys_clk_hz: 100000000", "sys_clk_hz: 125000000")'
arm recipe-contract-clock 1 'sub("tb/verilator/nvm_capture_cpu/recipe.py", "CPU_HZ = 50_000_000", "CPU_HZ = 62_500_000")'
arm contract-rate-payload-grows-bytes 1 'sub("scripts/nvm_contract.py", "\"RATE\": 4,", "\"RATE\": 8,")'
arm product-firmware-byte 1 'sub("sw/firmware/milan_baremetal/milan_baremetal.c", "static struct nvm_cap nvm_capture(void)", "static struct nvm_cap  nvm_capture(void)")'
arm planted-grader-ignores-off-limit 1 'sub("tb/verilator/nvm_capture_cpu/run.py", "        if row[\"sys_cycles\"] * 2000 >".replace(chr(34), chr(39)), "        if spec[\"traffic\"] == \"on\" and row[\"sys_cycles\"] * 2000 >".replace(chr(34), chr(39)))'
arm planted-maximum-on-only 1 'sub("tb/verilator/nvm_capture_cpu/run.py", "for arm in arms for row in arm[\"rows\"])".replace(chr(34), chr(39)), "for arm in arms if arm[\"traffic\"] == \"on\" for row in arm[\"rows\"])".replace(chr(34), chr(39)))'
arm receipt-drop-off-arm 1 'receipt(lambda r: r.__setitem__("measurements", [a for a in r["measurements"] if not (a["cpu_hz"] == 50000000 and a["traffic"] == "off" and a["shape"].endswith("8x8"))]))'
arm receipt-row-over-half-floor 1 'receipt(lambda r: r["measurements"][1]["rows"][0].__setitem__("sys_cycles", 2450001))'
arm receipt-maximum-edited-only 1 'receipt(lambda r: r["maxima"][1].__setitem__("maximum_ms", 24.0))'
arm receipt-measured-for-edited-only 1 'receipt(lambda r: r["measured_for"]["endstation_ax7101_8x8"].__setitem__("raw_bytes", 12000))'
# Honest residual: a self-consistent edit of rows, summaries and maxima passes,
# because the gate cannot prove that a simulation produced the numbers.
arm receipt-consistent-forgery 0 '
import importlib.util
sys.path[:0] = [str(root / "scripts"), str(root / "tb/verilator/nvm_capture_cpu")]
import run as cap, recipe
def forge(r):
    for a in r["measurements"]:
        for row in a["rows"]:
            row["sys_cycles"] = row["sys_cycles"] // 2
        a.update({k: v for k, v in cap.grade_rows(a["rows"], a).items() if k in a})
    new = []
    for m in r["maxima"]:
        g = [a for a in r["measurements"] if (a["shape"], a["cpu_hz"]) == (m["shape"], m["cpu_hz"])]
        w = cap.maximum_ms(g); new.append(dict(m, maximum_ms=w, margin=recipe.HOLD_FLOOR_MS / w))
    r["maxima"] = new
receipt(forge)'
cd "$CLONE" && echo "CLONE_STATUS $(git status --porcelain | wc -l) HEAD $(git rev-parse HEAD)"
