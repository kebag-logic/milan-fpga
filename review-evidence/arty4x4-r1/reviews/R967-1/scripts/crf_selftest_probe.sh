#!/bin/bash
# Apply the crf-frame-not-counted mutant to a disposable copy and run the service self-test's checks (no mutants).
# usage: crf_selftest_probe.sh CLONE PACKET
CLONE=$1; PKT=$2; T=$PKT/scratch/crf-tree; R=$PKT/receipts
rm -rf "$T"; mkdir -p "$T"; (cd "$CLONE" && tar --exclude=.git -cf - .) | (cd "$T" && tar -xf -)
cd "$T" || exit 2
python3 - <<'PY'
from pathlib import Path
p = Path('tb/verilator/ctrl_service_budget/egress_mii.py'); t = p.read_text()
assert t.count('    return aaf + crf\n') == 1
p.write_text(t.replace('    return aaf + crf\n', '    return aaf\n'))
PY
export PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 PATH=${PINNED_VERILATOR_DIR:?set PINNED_VERILATOR_DIR to the pinned Verilator 5.050 directory}:$PATH
python3 -B -c "import sys; sys.path.insert(0,'tb/verilator/ctrl_service_budget'); import selftest; selftest.selftest_mutants.MUTANTS={}; raise SystemExit(selftest.main([]))" > "$R/crf-mutant-service-checks.log" 2>&1
echo $? > "$R/crf-mutant-service-checks.rc"
python3 -B -c "import sys; sys.path.insert(0,'tb/verilator/ctrl_service_budget'); import egress_mii; print(egress_mii.params(dict(shape='endstation_arty_split_4x4', sys_hz=100_000_000, milan_hz=50_000_000)).sr_bytes)" >> "$R/crf-mutant-service-checks.log" 2>&1
cd "$PKT"; rm -rf "$T"
