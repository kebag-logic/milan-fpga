#!/bin/bash
# chainC: every docs.yml job, then every elaborate.yml job, each on its own fresh clone of the gate head, in turn
G=$VALIDATION_STORAGE/665s8-a758b/gates; export CPUS=116-119
$G/docs_jobs.sh
$G/wf_jobs.sh elaborate $G/elaborate elaborate-gates-0:litex elaborate-gates-1:litex elaborate ci-manifest ci-fail-fast ci-cancel-tail
echo done > $G/chainC.done
