#!/usr/bin/env bash
# every job of .github/workflows/docs.yml at <sha>, each on a fresh clone, then the verifier
set -u
H=$1; R=<scratch>/gates/docsyml-$(echo $1 | cut -c1-8)
mkdir -p "$R"
for job in wire-accountability docs-check-no-git docs-gates-0 docs-gates-1 docs-gates-2 docs-check ci-manifest ci-fail-fast ci-cancel-tail; do
  /usr/bin/python3 <scratch>/gates/tools/run_docs_yml.py "$H" "$job" "$R" >> "$R/runner.out" 2>&1
  echo "$job runner rc=$?" >> "$R/runner.out"
done
/usr/bin/python3 <scratch>/gates/tools/verify_docs_yml.py "$H" "$R" > "$R/verify.md" 2>&1
echo "$?" > "$R/verify.rc"
echo done > "$R/DONE"
