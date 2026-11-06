#!/usr/bin/env bash
# docs_jobs.sh <head sha> [job ...]: the named jobs of .github/workflows/docs.yml at the head (every job when none is
# named) through run_docs_yml.py, one fresh clone per job, then verify_docs_yml.py's table once every job has run.
# Logs and rc files under the scratch root's logs/.
set -u
H=$1; shift; R=$VALIDATION_STORAGE/839-a731c/docsyml-${H:0:8}${DOCS_ROOT_SUFFIX:-}
T=$MANAGEMENT/2026-09-23/839-a731c/receipts/gates/tools
PY=$VALIDATION_STORAGE/839-a731b/gates/venv/bin/python3
mkdir -p "$R"
jobs="$*"
[ -n "$jobs" ] || jobs=$(git -C $LANES/839-boot-sa show "$H:.github/workflows/docs.yml" | $PY -c 'import sys, yaml; print(" ".join(yaml.safe_load(sys.stdin)["jobs"]))')
for job in $jobs; do
  $PY "$T/run_docs_yml.py" "$H" "$job" "$R" > "$R/$job.runner.out" 2>&1
  echo "$job runner rc=$?"
done
$PY "$T/verify_docs_yml.py" "$H" "$R" > "$R/docs-yml-table.md" 2>&1
echo $? > "$R/verify.rc"
echo "verify rc=$(cat "$R/verify.rc")"
