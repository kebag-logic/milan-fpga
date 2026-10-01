#!/usr/bin/env bash
# R410-3 probe: the driver's validator names re-anchored to F30 are load-bearing.
# In a disposable clone of the head, revert only the driver's two rx_validator
# names to the pre-merge "F29 ..." and run cdl_not_44_rejected: the validator
# record must turn SURVIVED with both names missing (the planted defect is the
# same; only the anchor moved). The head's driver KILLS it (receipts).
#   probe_reanchor.sh HEAD_REPO VBIN OUT SCRATCH
set -uo pipefail
repo=$1; vbin=$2; out=$3; scratch=$4
export PATH="$vbin:$PATH" TMPDIR="$scratch/tmp"; mkdir -p "$TMPDIR" "$out"
rm -rf "$scratch/probe-reanchor"
git clone -q --no-checkout "$repo" "$scratch/probe-reanchor" && cd "$scratch/probe-reanchor" || exit 2
git checkout -q --detach 4e558491c608dc88efc7963a77cb6b49bce2a46e
python3 - <<'PY'
from pathlib import Path
p = Path("tb/pp_top/acmp_mutants.py"); s = p.read_text()
old = '("F30 BIND_RX cdl 84", "F30 PROBE_TX cdl 84")'
assert s.count(old) == 1
p.write_text(s.replace(old, '("F29 BIND_RX cdl 84", "F29 PROBE_TX cdl 84")'))
PY
git diff --stat > "$out/reanchor-probe.diffstat"
taskset -c 0-7 python3 tb/pp_top/acmp_mutants.py --output "$out/reanchor-probe" --verilator "$vbin/verilator" --jobs 2 --only cdl_not_44_rejected > "$out/reanchor-probe.log" 2>&1
echo "probe rc=$? (expected 1: one record SURVIVED)" | tee -a "$out/reanchor-probe.log"
