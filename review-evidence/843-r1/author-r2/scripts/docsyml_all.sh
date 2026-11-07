#!/usr/bin/env bash
# docsyml_all.sh <head> <root>: every job of docs.yml at <head>, one after the other, each on its own fresh clone,
# then the verifier over every run: step of the workflow. Exit status of the verifier is the result.
set -u
H=$1; R=$2; T=$(cd "$(dirname "$0")" && pwd)
mkdir -p "$R"
for job in wire-accountability docs-check-no-git docs-gates-0 docs-gates-1 docs-gates-2 docs-check ci-manifest ci-fail-fast ci-cancel-tail; do
  /usr/bin/python3 -I "$T/run_docs_yml.py" "$H" "$job" "$R" >> "$R/runner.out" 2>&1
  echo "$job runner rc=$?" >> "$R/runner.out"
done
/usr/bin/python3 -I "$T/verify_docs_yml.py" "$H" "$R" > "$R/docs-yml-table.md" 2>&1
echo $? > "$R/verify.rc"
echo done > "$R/ALL_DONE"
