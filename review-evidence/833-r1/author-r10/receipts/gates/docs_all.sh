#!/usr/bin/env bash
# Every docs.yml job with a local gate, each on a fresh clean clone of the head, one log and rc per step.
set -u
G=$VALIDATION_STORAGE/833-a726j/gates
H=fce77f0efc1425ef7732a8d70c02addc108f7afe
mkdir -p $G/run1
grep SigIgn /proc/$$/status > $G/run1/sigign.txt
cat /proc/loadavg > $G/run1/load.txt
for job in wire-accountability docs-check-no-git docs-gates-0 docs-gates-1 docs-gates-2; do
  date +%T > $G/run1/$job.start
  $G/venv/bin/python3 -I $G/tools/run_docs_yml.py $H $job $G/run1
  echo $? > $G/run1/$job.runner-rc
  date +%T > $G/run1/$job.end
  cat /proc/loadavg >> $G/run1/load.txt
done
$G/venv/bin/python3 -I $G/tools/verify_docs_yml.py $H $G/run1 > $G/run1/docsyml-table.md 2>&1
echo $? > $G/run1/docsyml-verify.rc
cat /proc/loadavg >> $G/run1/load.txt
echo done > $G/run1/ALLDONE
