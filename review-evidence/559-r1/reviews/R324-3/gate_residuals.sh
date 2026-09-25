#!/usr/bin/env bash
# R324-3: inputs OUTSIDE scripts/check_nvm_capture.py's stated scope (census,
# clocks, firmware and harness hashes). Each arm is expected to PASS the gate;
# the result documents what the gate does not protect. Scratch copy only.
# Usage: CLONE=<exact-head clone> bash gate_residuals.sh
set -uo pipefail
PKT=$(cd "$(dirname "$0")" && pwd)
: "${CLONE:?set CLONE to the exact-head review clone}"
R=$PKT/scratch/repo_res; rm -rf "$R"; cp -a "$CLONE" "$R"; cd "$R"
arm() {
  python3 - <<PY
from pathlib import Path
p = Path('$2'); s = p.read_text(); assert s.count('''$3''') == 1, '$2'
p.write_text(s.replace('''$3''', '''$4'''))
PY
  out=$(python3 scripts/check_nvm_capture.py 2>&1); rc=$?
  echo "RESIDUAL $1 gate_rc=$rc :: $(printf '%s\n' "$out" | grep -m1 -E '^(FAIL|PASS)' | cut -c1-120)"
  git checkout -q -- . && [ -z "$(git status --porcelain)" ] || echo "RESTORE FAILED $1"
}
arm backend-hold-50-to-30ms hdl/milan/KL_nvm_backend.sv 'parameter int unsigned T_HOLD_MS_P    = 50,' 'parameter int unsigned T_HOLD_MS_P    = 30,'
arm soc-cpu-memory-crossing-edit sw/litex/milan_soc.py 'def pp_mem_bus_worst_cycles(sys_clk_hz: float) -> int:' 'def pp_mem_bus_worst_cycles(sys_clk_hz: float) -> int:  # edited'
cd "$CLONE" && echo "CLONE_STATUS $(git status --porcelain | wc -l) HEAD $(git rev-parse HEAD)"
