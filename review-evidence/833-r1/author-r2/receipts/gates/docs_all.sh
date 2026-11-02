#!/usr/bin/env bash
# Every docs.yml job with a local gate, each on a fresh clean clone of the head, one log and rc per step.
set -u
for job in wire-accountability docs-check-no-git docs-gates-0 docs-gates-1 docs-gates-2; do
  $VALIDATION_STORAGE/833-a726b/gates/venv/bin/python3 -I $VALIDATION_STORAGE/833-a726b/gates/tools/run_docs_yml.py 1ff8292cd5b761633ef9500a7c5a4b1626a3d92c $job $VALIDATION_STORAGE/833-a726b/gates/run1
done
$VALIDATION_STORAGE/833-a726b/gates/venv/bin/python3 -I $VALIDATION_STORAGE/833-a726b/gates/tools/verify_docs_yml.py 1ff8292cd5b761633ef9500a7c5a4b1626a3d92c $VALIDATION_STORAGE/833-a726b/gates/run1 > $VALIDATION_STORAGE/833-a726b/gates/run1/docsyml-table.md 2>&1
echo $? > $VALIDATION_STORAGE/833-a726b/gates/run1/docsyml-verify.rc
echo done > $VALIDATION_STORAGE/833-a726b/gates/run1/ALLDONE
