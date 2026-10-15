#!/usr/bin/env bash
# Reviewer mutation probe: apply one textual mutation to a tracked file in the
# given checkout, run the committed gate self-test, record rc, restore the file.
# Usage: mutation_probe.sh <checkout> <outdir>
set -u
repo=$1; out=$2
cd "$repo"
probe() {  # label file python-replacement-old python-replacement-new
  label=$1 file=$2 old=$3 new=$4
  python3 - "$file" "$old" "$new" <<'EOF' || { echo "$label: mutation did not apply" >> "$out/mutations.txt"; return; }
import sys
path, old, new = sys.argv[1:]
text = open(path).read()
assert text.count(old) == 1, ("anchor count", text.count(old))
open(path, "w").write(text.replace(old, new))
EOF
  start=$(date +%s)
  python3 scripts/ci_gate_workflows_selftest.py > "$out/mut-$label.log" 2>&1; rc=$?
  git checkout -- "$file"
  echo "$label rc=$rc seconds=$(( $(date +%s) - start )) last: $(grep -v '^\s*$' "$out/mut-$label.log" | tail -1 | cut -c1-200)" >> "$out/mutations.txt"
}
: > "$out/mutations.txt"
python3 scripts/ci_gate_workflows_selftest.py > "$out/mut-pristine.log" 2>&1
echo "pristine rc=$?" >> "$out/mutations.txt"
# M1: requirement-flag parser accepts repeated and unknown flags
probe M1-requirements-unchecked scripts/ci_builder_legs.py \
  '    if not set(flags) <= set(REQUIRED) or len(set(flags)) != len(flags):' \
  '    if False:'
# M2: docs builder legs swapped between workers 1 and 2
probe M2-docs-workers-swapped scripts/ci_gate_workflows.py \
  'BUILDER_WORKERS = {"docs": (1, 2), "elaborate": (0, 1)}' \
  'BUILDER_WORKERS = {"docs": (2, 1), "elaborate": (0, 1)}'
# M3: docs workers stop retaining builder-leg receipts
probe M3-docs-receipts-not-uploaded scripts/ci_gate_workflows.py \
  '    if leg in BUILDER_WORKERS[name]:' \
  '    if name == "elaborate":'
# M4: production aggregate judges every requirement regardless of the command
probe M4-aggregate-judges-both scripts/ci_gate_receipts.py \
  '        union(builder or [], identity[0], identity[1], requirements(builder_command(name, source)))' \
  '        union(builder or [], identity[0], identity[1], ["--require-elaboration", "--require-rv32"])'
# M5: per-leg requirement equality removed from the union
probe M5-no-per-leg-equality scripts/ci_builder_legs.py \
  '        if sorted(receipt["driver"]["requirements"]) != sorted(flags):' \
  '        if False:'
# M6: the divided step may hide the driver in a preparation line
probe M6-preparation-driver-unchecked scripts/ci_gate_workflows.py \
  '            or any("sw/builder/test_builder.py" in line for line in preparation)):' \
  '            ):'
python3 scripts/ci_gate_workflows_selftest.py > "$out/mut-pristine-after.log" 2>&1
echo "pristine-after rc=$?" >> "$out/mutations.txt"
git status --short --untracked-files=no >> "$out/mutations.txt"
