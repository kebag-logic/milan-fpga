#!/usr/bin/env bash
# Every job of .github/workflows/docs.yml at <head>, each on its own fresh clone
# (run_docs_yml.py), then the verifier's table. Usage: docs_battery.sh <head> <scratch>
set -u
head=$1; root=$2
here=$(dirname "$(readlink -f "$0")")
mkdir -p "$root"
for job in wire-accountability docs-check-no-git docs-gates-0 docs-gates-1 docs-gates-2 docs-check ci-manifest ci-fail-fast ci-cancel-tail; do
  echo "JOB $job start $(date -Is)"
  python3 "$here/run_docs_yml.py" "$head" "$job" "$root"
  echo "JOB $job end rc=$? $(date -Is)"
done
python3 "$here/verify_docs_yml.py" "$head" "$root" > "$root/docs-yml-table.md"
echo "VERIFY rc=$? $(date -Is)"
