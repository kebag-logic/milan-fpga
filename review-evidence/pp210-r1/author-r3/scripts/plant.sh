#!/usr/bin/env bash
# Plant each restated-count mutant in a disposable clone, run `make inventory`,
# restore the clone after each. usage: plant.sh <clone> <log>
set -u
cd "$1" || exit 1
L=$2
: > "$L"
run() {
  echo "== $1" >> "$L"
  make inventory >> "$L" 2>&1
  echo "rc $?" >> "$L"
  git checkout -q -- .
  git status --short >> "$L"
}
make inventory > /dev/null 2>&1; echo "control rc $?" >> "$L"
sed -i 's/a different ISA, the `ucpu_op_e` enum in/a different 29-operation ISA in/' IEEE_1722_1_Hardware_Protocol_Processor.md
run "M1 concept banner back to its 0ea635e text, 29-operation"
sed -i 's/a different ISA, the `ucpu_op_e` enum in/a different 30-operation ISA, the `ucpu_op_e` enum in/' IEEE_1722_1_Hardware_Protocol_Processor.md
run "M2 concept banner states the true count, 30-operation"
printf '\nThe µCPU runs the 30 operations of the µISA.\n' >> tb/ucpu/README.md
run "M3 a current page restates 30 operations of the µISA"
sed -i 's/^\*\*µISA (30 operations)\*\*/**µISA (30 operations)** (the µISA has 30 ops)/' docs/architecture/06_aecp_engine.md
run "M4 06 restates the count beside its derived heading"
sed -i 's/a different ISA, the `ucpu_op_e` enum in/a different 29-operation ISA in/' IEEE_1722_1_Hardware_Protocol_Processor.md
git show 0ea635e:scripts/check-doc-inventory.py > scripts/check-doc-inventory.py
run "M5 M1 under the round-2 gate script (0ea635e)"
sed -i '536s/29 operations/31 operations/' docs/10_RESOURCE_AND_EFFORT.md
git diff --stat >> "$L"
run "C1 control: a retired page's body (10 :536) changes its historical count"
make inventory > /dev/null 2>&1; echo "end control rc $?" >> "$L"
git rev-parse HEAD >> "$L"
git status --short >> "$L"
