#!/bin/bash
# Resume docs.yml at a head after a host reset: the killed job's partial clone and logs moved aside into ROOT/killed,
# then that job and every job after it in docsrun.sh's order, each on its fresh clone, then the verifier over ROOT.
# usage: docsrest.sh HEAD ROOT FIRST_JOB
set -u
H=$1 R=$2 FIRST=$3
S=$MANAGEMENT/2026-09-23/665s2b-a683u/scripts
go=
for job in wire-accountability docs-check-no-git docs-gates-0 docs-gates-1 docs-gates-2 docs-check; do
    [ "$job" = "$FIRST" ] && go=1
    [ -n "$go" ] || continue
    if [ -e "$R/$job" ] || ls "$R/logs/${job}__"* > /dev/null 2>&1; then
        mkdir -p "$R/killed/logs"
        [ -e "$R/$job" ] && mv "$R/$job" "$R/killed/"
        [ -e "$R/$job.driver.log" ] && mv "$R/$job.driver.log" "$R/killed/"
        mv "$R/logs/${job}__"* "$R/killed/logs/" 2>/dev/null
        echo "$job moved aside (killed by a host reset)" >> "$R/jobs.txt"
    fi
    $VALIDATION_STORAGE/665s2b-a683u/gates/venv/bin/python3 "$S/run_docs_yml.py" "$H" "$job" "$R" > "$R/$job.driver.log" 2>&1
    echo "$job rc=$?" >> "$R/jobs.txt"
done
$VALIDATION_STORAGE/665s2b-a683u/gates/venv/bin/python3 "$S/verify_docs_yml.py" "$H" "$R" > "$R/verify.log" 2>&1
echo "verify rc=$?" >> "$R/jobs.txt"
echo done >> "$R/jobs.txt"
