#!/usr/bin/env bash
# docs-check-no-git replica: run inside a `git archive` export of the candidate (no .git).
set -u
[ ! -e .git ] || { echo "refusing: .git present"; exit 2; }
python3 -B scripts/docs_check.py; a=$?
python3 scripts/check_feature_status.py; b=$?
echo "docs_check=$a check_feature_status=$b"
[ $a -eq 0 ] && [ $b -eq 0 ]
