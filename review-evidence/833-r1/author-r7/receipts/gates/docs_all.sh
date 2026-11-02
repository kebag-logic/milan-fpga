#!/usr/bin/env bash
# Every docs.yml job with a local gate, each on a fresh clean clone of the head, one log and rc per step.
set -u
grep SigIgn /proc/$$/status > $VALIDATION_STORAGE/833-a726g/gates/run1/sigign.txt
for job in wire-accountability docs-check-no-git docs-gates-0 docs-gates-1 docs-gates-2; do
  $VALIDATION_STORAGE/833-a726g/gates/venv/bin/python3 -I $VALIDATION_STORAGE/833-a726g/gates/tools/run_docs_yml.py 887fdd53b013cc8796c1d595644a2a9f0b8c27a5 $job $VALIDATION_STORAGE/833-a726g/gates/run1
done
$VALIDATION_STORAGE/833-a726g/gates/venv/bin/python3 -I $VALIDATION_STORAGE/833-a726g/gates/tools/verify_docs_yml.py 887fdd53b013cc8796c1d595644a2a9f0b8c27a5 $VALIDATION_STORAGE/833-a726g/gates/run1 > $VALIDATION_STORAGE/833-a726g/gates/run1/docsyml-table.md 2>&1
echo $? > $VALIDATION_STORAGE/833-a726g/gates/run1/docsyml-verify.rc
echo done > $VALIDATION_STORAGE/833-a726g/gates/run1/ALLDONE
