#!/usr/bin/env bash
# Every run: step of docs.yml at the head, job by job, sequentially, each on its own fresh clone; then the lane steps.
set -u
echo $$ > $VALIDATION_STORAGE/640-a720p/gates/run_all.pid
date -Is > $VALIDATION_STORAGE/640-a720p/gates/run_all.start
H=72816d26a7e2a29db5bc198ff65056ee4c5790b4
for job in wire-accountability docs-check-no-git docs-gates-0 docs-gates-1 docs-gates-2; do
  $VALIDATION_STORAGE/640-a720p/venv/bin/python3 -I $VALIDATION_STORAGE/640-a720p/tools/run_docs_yml.py $H $job $VALIDATION_STORAGE/640-a720p/gates
done
bash $VALIDATION_STORAGE/640-a720p/tools/run_extra.sh $H
$VALIDATION_STORAGE/640-a720p/venv/bin/python3 -I $VALIDATION_STORAGE/640-a720p/tools/verify_docs_yml.py $H $VALIDATION_STORAGE/640-a720p/gates > $VALIDATION_STORAGE/640-a720p/gates/verify.md; echo $? > $VALIDATION_STORAGE/640-a720p/gates/verify.rc
date -Is > $VALIDATION_STORAGE/640-a720p/gates/run_all.end
