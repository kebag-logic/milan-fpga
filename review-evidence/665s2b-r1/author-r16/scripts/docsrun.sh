#!/bin/bash
# Every job of docs.yml at a head, each on its fresh clone, one after another. usage: docsrun.sh HEAD ROOT
set -u
H=$1 R=$2
S=$MANAGEMENT/2026-09-23/665s2b-a683u/scripts
mkdir -p "$R"
for job in wire-accountability docs-check-no-git docs-gates-0 docs-gates-1 docs-gates-2 docs-check; do
    $VALIDATION_STORAGE/665s2b-a683u/gates/venv/bin/python3 "$S/run_docs_yml.py" "$H" "$job" "$R" > "$R/$job.driver.log" 2>&1
    echo "$job rc=$?" >> "$R/jobs.txt"
done
$VALIDATION_STORAGE/665s2b-a683u/gates/venv/bin/python3 "$S/verify_docs_yml.py" "$H" "$R" > "$R/verify.log" 2>&1
echo "verify rc=$?" >> "$R/jobs.txt"
echo done >> "$R/jobs.txt"
