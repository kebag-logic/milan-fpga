#!/bin/sh
# Usage: probe_gate_read.sh <repository root at the head> <empty scratch dir>.
# Mutates the gate-read policy table in a disposable copy and runs the resource gate's check-baseline.
root=$1; d=$2; set -u
git -C "$root" archive HEAD docs/design/AREA_BUDGET.md syn/ooc scripts | tar -x -C "$d"
cp "$d/docs/design/AREA_BUDGET.md" "$d/AB.orig"
cd "$d"
python3 syn/ooc/pp_resource_gate.py check-baseline; echo "control unmutated rc=$?"
sed -i '/^| Endpoint | LUT/,/^$/s/^| `route-1x1` | +500 /| `route-1x1` | +7 /' docs/design/AREA_BUDGET.md
python3 syn/ooc/pp_resource_gate.py check-baseline; echo "mutant A, route LUT tolerance in the policy table, rc=$?"
cp AB.orig docs/design/AREA_BUDGET.md
sed -i 's/^| Endpoint | LUT/| Endpoint |  LUT/' docs/design/AREA_BUDGET.md
python3 syn/ooc/pp_resource_gate.py check-baseline; echo "mutant B, table header, rc=$?"
