#!/bin/bash
# Every job of docs.yml at a head, each on its fresh clone, one after another.
set -u
H=$1 R=$2
for job in wire-accountability docs-check-no-git docs-gates-0 docs-gates-1 docs-gates-2 docs-check; do
    $VALIDATION_STORAGE/665s2b-a683o/gates/venv/bin/python3 $MANAGEMENT/2026-09-23/665s2b-a683p/scripts/run_docs_yml.py "$H" "$job" "$R" > "$R/$job.driver.log" 2>&1
    echo "$job rc=$?" >> "$R/jobs.txt"
done
echo done >> "$R/jobs.txt"
