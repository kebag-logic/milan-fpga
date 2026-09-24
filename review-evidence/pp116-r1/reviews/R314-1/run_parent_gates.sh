#!/usr/bin/env bash
# Run the three parent docs-check gates named by processor issue #116 in a
# parent consumer tree. Usage: run_parent_gates.sh <parent-tree> <label> <outdir>
# The parent tree must be kebag-logic/milan-fpga at 508-pp-pin-adopt
# (35f06958) with protocol-processor and gptp-processor working trees
# populated at their gitlinks. Writes <outdir>/<label>.<gate>.log and
# <outdir>/<label>.exits (one "gate exit" line per gate).
set -u
tree=$1; label=$2; out=$3
mkdir -p "$out"
: > "$out/$label.exits"
cd "$tree" || exit 2
# The gates refuse uninitialised submodules; register the two populated ones.
git submodule init protocol-processor gptp-processor > /dev/null
{
  echo "parent HEAD $(git rev-parse HEAD)"
  echo "gitlink protocol-processor $(git ls-tree HEAD protocol-processor | awk '{print $3}')"
  echo "checked-out protocol-processor $(git -C protocol-processor rev-parse HEAD)"
  echo "checked-out gptp-processor $(git -C gptp-processor rev-parse HEAD)"
} > "$out/$label.identity"
run() {
  name=$1; shift
  python3 -I "$@" > "$out/$label.$name.log" 2>&1
  echo "$name $?" >> "$out/$label.exits"
}
run check_port_contracts scripts/check_port_contracts.py
run measure_naming_check scripts/measure_naming.py --check
run measure_test_evidence_check scripts/measure_test_evidence.py --check
cat "$out/$label.identity" "$out/$label.exits"
