#!/bin/bash
# Every docs.yml job from the workflow's own list, on its own clean clone of the head.
S=$VALIDATION_STORAGE/829-a725e; H=b9628c8963d436af0dccebb205a5241ece5d9e93; R=$S/gates/run1; V=$VALIDATION_STORAGE/829-a725c/gates/venv/bin/python3; RUN=$S/gates/run_docs_yml.py
export TMPDIR=$S/tmp
mkdir -p $TMPDIR
for j in wire-accountability docs-check-no-git; do $V $RUN $H $j $R > $R/$j.out 2>&1; echo "$j rc=$?" >> $R/driver.log; done
for j in docs-gates-0 docs-gates-1 docs-gates-2; do ( $V $RUN $H $j $R > $R/$j.out 2>&1; echo "$j rc=$?" >> $R/driver.log ) & done
wait
touch $R/DONE
