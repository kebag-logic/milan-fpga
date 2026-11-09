#!/usr/bin/env bash
# Every run: step of docs.yml at the head, job by job, sequentially, each on its own fresh clone; then the lane steps.
set -u
S=$VALIDATION_STORAGE/640-a720q; G=$S/gates
mkdir -p $G
echo $$ > $G/run_all.pid
date -Is > $G/run_all.start
H=e70ae2cb2dd0746060612493cb6724522b8701bc
for job in wire-accountability docs-check-no-git docs-gates-0 docs-gates-1 docs-gates-2; do
  $S/venv/bin/python3 -I $S/tools/run_docs_yml.py $H $job $G
done
bash $S/tools/run_extra.sh $H
$S/venv/bin/python3 -I $S/tools/verify_docs_yml.py $H $G > $G/verify.md; echo $? > $G/verify.rc
date -Is > $G/run_all.end
