#!/bin/bash
# docs.yml's three jobs (docs-check, wire-accountability, docs-check-no-git),
# every step, in sequence, each in its own HOME, after the milan_dp work:
# docs-check's self-tests rewrite tracked files that builds read.
set -u
R=$VALIDATION_STORAGE/629-a517
O=$HOME/milan-fpga-management/2026-09-23/629-a517/scripts
for job in docs-check wire-accountability docs-check-no-git; do
  mkdir -p "$R/home-$job"
  echo "$job start $(date -Is)"
  HOMEDIR=$R/home-$job "$O/run_job.sh" .github/workflows/docs.yml "$job" "$job"
  echo "$job rc=$? end $(date -Is)"
done
echo "porcelain after: $(git -C $LANES/629-m2-impl status --porcelain | wc -l)"
