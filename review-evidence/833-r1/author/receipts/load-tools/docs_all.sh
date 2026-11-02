#!/usr/bin/env bash
# Every docs.yml job with a local gate, each on a fresh clean clone of the head, one log and rc per step.
set -u
for job in wire-accountability docs-check-no-git docs-gates-0 docs-gates-1 docs-gates-2; do
  python3 $VALIDATION_STORAGE/833-a726/gates/tools/run_docs_yml.py d4d8cff92658e57b11090c97daf7b44edb31b3b6 $job $VALIDATION_STORAGE/833-a726/gates/run5
done
echo done > $VALIDATION_STORAGE/833-a726/gates/run5/ALLDONE
