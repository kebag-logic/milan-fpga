#!/bin/bash
# docs_jobs.sh: every docs.yml job on its own fresh clone of the gate head, in turn
: "${CPUS:?CPUS unset}"
G=$VALIDATION_STORAGE/665s8-a758b/gates; H=$(cat $G/HEAD)
for job in wire-accountability docs-check-no-git docs-gates-0 docs-gates-1 docs-gates-2 docs-check ci-manifest ci-fail-fast ci-cancel-tail; do
  start=$(date +%s)
  taskset -c "$CPUS" $VALIDATION_TOOLS/md-venv-40cdefe08ebd/bin/python3 $G/run_docs_yml.py "$H" "$job" $G/docs >> $G/docs/driver.log 2>&1
  echo "$job $? $(( $(date +%s) - start ))s" >> $G/docs/jobs.txt
done
echo done >> $G/docs/jobs.txt
