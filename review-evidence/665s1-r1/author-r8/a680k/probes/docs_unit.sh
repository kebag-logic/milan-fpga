#!/bin/bash
# The docs workflow's gates at the lane head, into receipts/gates/docs-gates.txt (system python, TMPDIR on disk).
export TMPDIR=$VALIDATION_STORAGE/scratch/665s1-a680k-work/tmp
O=$MANAGEMENT/2026-09-23/665s1-a680k
git -C $LANES/665-s1-faces rev-parse HEAD > "$O/receipts/gates/docs-gates.txt.head"
"$O/probes/run_gate.sh" "$O/receipts/gates/docs-gates.txt" bash "$O/probes/docs_gates.sh" $LANES/665-s1-faces \
  $VALIDATION_TOOLS/md-venv/lib/python3.14/site-packages:$VALIDATION_STORAGE/scratch/a680b-work/hdlref-venv/lib/python3.14/site-packages
