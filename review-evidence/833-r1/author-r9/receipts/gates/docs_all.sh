#!/usr/bin/env bash
# Every docs.yml job with a local gate, each on a fresh clean clone of the head, one log and rc per step.
set -u
mkdir -p $VALIDATION_STORAGE/833-a726i/gates/run1
grep SigIgn /proc/$$/status > $VALIDATION_STORAGE/833-a726i/gates/run1/sigign.txt
cat /proc/loadavg > $VALIDATION_STORAGE/833-a726i/gates/run1/load.txt
for job in wire-accountability docs-check-no-git docs-gates-0 docs-gates-1 docs-gates-2; do
  date +%T > $VALIDATION_STORAGE/833-a726i/gates/run1/$job.start
  $VALIDATION_STORAGE/833-a726i/gates/venv/bin/python3 -I $VALIDATION_STORAGE/833-a726i/gates/tools/run_docs_yml.py e803d94b3a11921a293cf036a8eda333d23828f9 $job $VALIDATION_STORAGE/833-a726i/gates/run1
  echo $? > $VALIDATION_STORAGE/833-a726i/gates/run1/$job.runner-rc
  date +%T > $VALIDATION_STORAGE/833-a726i/gates/run1/$job.end
done
$VALIDATION_STORAGE/833-a726i/gates/venv/bin/python3 -I $VALIDATION_STORAGE/833-a726i/gates/tools/verify_docs_yml.py e803d94b3a11921a293cf036a8eda333d23828f9 $VALIDATION_STORAGE/833-a726i/gates/run1 > $VALIDATION_STORAGE/833-a726i/gates/run1/docsyml-table.md 2>&1
echo $? > $VALIDATION_STORAGE/833-a726i/gates/run1/docsyml-verify.rc
cat /proc/loadavg >> $VALIDATION_STORAGE/833-a726i/gates/run1/load.txt
echo done > $VALIDATION_STORAGE/833-a726i/gates/run1/ALLDONE
