#!/bin/bash
# rerun_gptp.sh: #833 (a suite-cancellation preflight timeout): physical-gptp once more on a fresh clone, both results kept
G=$VALIDATION_STORAGE/665s8-a758b/gates; export CPUS=104-107
cd $G/rtl && mkdir -p first-attempt-gptp && mv physical-gptp first-attempt-gptp/ && for f in logs/rtl__physical-gptp__*; do mv "$f" first-attempt-gptp/; done
$G/wf_jobs.sh rtl $G/rtl physical-gptp
echo done > $G/rerun_gptp.done
