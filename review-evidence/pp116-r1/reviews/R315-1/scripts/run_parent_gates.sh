#!/bin/sh
# Run the three parent docs-check gates named by processor issue #116 in a
# parent consumer checkout (kebag-logic/milan-fpga, branch 508-pp-pin-adopt).
#   usage: run_parent_gates.sh <parent-checkout> <label> <outdir>
# Records each gate's full output and exit status plus the parent HEAD and
# the protocol-processor gitlink/checkout identity it ran against.
set -u
parent=$1; label=$2; out=$3
mkdir -p "$out"
cd "$parent" || exit 2
{
  echo "parent_head=$(git rev-parse HEAD)"
  echo "gitlink=$(git ls-tree HEAD protocol-processor | awk '{print $3}')"
  echo "pp_checkout=$(git -C protocol-processor rev-parse HEAD)"
  echo "pp_tree=$(git -C protocol-processor rev-parse 'HEAD^{tree}')"
  echo "pp_dirty=$(git -C protocol-processor status --porcelain | wc -l)"
  echo "budget_sha256=$(sha256sum scripts/test_evidence.budget | cut -d' ' -f1)"
} > "$out/$label.identity"
python3 scripts/check_port_contracts.py > "$out/$label.check_port_contracts.log" 2>&1
echo "check_port_contracts rc=$?" > "$out/$label.rc"
python3 scripts/measure_naming.py --check > "$out/$label.measure_naming.log" 2>&1
echo "measure_naming_check rc=$?" >> "$out/$label.rc"
python3 scripts/measure_test_evidence.py --check > "$out/$label.measure_test_evidence.log" 2>&1
echo "measure_test_evidence_check rc=$?" >> "$out/$label.rc"
cat "$out/$label.identity" "$out/$label.rc"
