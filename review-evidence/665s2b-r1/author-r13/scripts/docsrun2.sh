#!/bin/bash
# The given jobs of docs.yml at a head, each on its fresh clone, one after another.
# usage: docsrun2.sh HEAD ROOT JOB...
set -u
H=$1 R=$2; shift 2
for job in "$@"; do
    $VALIDATION_STORAGE/665s2b-a683o/gates/venv/bin/python3 $MANAGEMENT/2026-09-23/665s2b-a683p/scripts/run_docs_yml.py "$H" "$job" "$R" > "$R/$job.driver.log" 2>&1
    echo "$job rc=$?" >> "$R/jobs.txt"
done
