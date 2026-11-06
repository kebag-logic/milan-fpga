#!/usr/bin/env bash
# docs_all.sh <head> <root>: every job of docs.yml at <head>, one after the other, each on its own fresh clone,
# empty HOME and new venv, then the verifier over every run: step of the workflow.
set -u
H=$1; R=$2; T=$MANAGEMENT/2026-09-23/665s4-a698h/scripts
PY=$VALIDATION_STORAGE/scratch/665s4-a698h/docs312/bin/python3
mkdir -p "$R"
for job in wire-accountability docs-check-no-git docs-gates-0 docs-gates-1 docs-gates-2 docs-check ci-manifest ci-fail-fast ci-cancel-tail; do
  "$PY" -I "$T/run_docs_yml.py" "$H" "$job" "$R" >> "$R/runner.out" 2>&1
  echo "$job runner rc=$?" >> "$R/runner.out"
done
"$PY" -I "$T/verify_docs_yml.py" "$H" "$R" > "$R/docs-yml-table.md" 2>&1
echo $? > "$R/verify.rc"
