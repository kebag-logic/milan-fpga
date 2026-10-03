#!/bin/bash
# docs.yml's docs-check job, every step, in its own HOME.
set -u
R=$VALIDATION_STORAGE/629-a512
O=$HOME/milan-fpga-management/2026-09-23/629-a512/scripts
mkdir -p "$R/home-docs"
echo "docs-check start $(date -Is)"
HOMEDIR=$R/home-docs "$O/run_job.sh" .github/workflows/docs.yml docs-check docs-check
echo "docs-check rc=$? end $(date -Is)"
