#!/bin/bash
# rerun_elab1.sh: elaborate-gates-1 once more on a fresh clone (its gate_19 timed out, result unknown), both results kept
G=$VALIDATION_STORAGE/665s8-a758b/gates; export CPUS=116-119
cd $G/elaborate && mkdir -p first-attempt-gates-1 && mv elaborate-gates-1 first-attempt-gates-1/ && for f in logs/elaborate__elaborate-gates-1__*; do mv "$f" first-attempt-gates-1/; done
$G/wf_jobs.sh elaborate $G/elaborate elaborate-gates-1:litex
echo done > $G/rerun_elab1.done
