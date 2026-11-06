#!/bin/bash
# One docs.yml job again at a head, on its fresh clone, then the verifier over ROOT. usage: docsone.sh HEAD ROOT JOB
set -u
H=$1 R=$2 JOB=$3
S=$MANAGEMENT/2026-09-23/665s2b-a683u/scripts
$VALIDATION_STORAGE/665s2b-a683u/gates/venv/bin/python3 "$S/run_docs_yml.py" "$H" "$JOB" "$R" > "$R/$JOB.driver.log" 2>&1
echo "$JOB rc=$?" >> "$R/jobs.txt"
$VALIDATION_STORAGE/665s2b-a683u/gates/venv/bin/python3 "$S/verify_docs_yml.py" "$H" "$R" > "$R/verify.log" 2>&1
echo "verify rc=$?" >> "$R/jobs.txt"
echo done >> "$R/jobs.txt"
