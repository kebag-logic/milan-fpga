#!/bin/bash
# The light jobs in sequence: rtl-fast's changes, verilator-lint and
# bdd-conformance; rtl.yml's full-ci-gate; docs.yml's wire-accountability and
# docs-check-no-git. They ran while Vivado routed (place/route needs ~6 GB).
set -u
R=$VALIDATION_STORAGE/629-a512
O=$HOME/milan-fpga-management/2026-09-23/629-a512/scripts
mkdir -p "$R/home-light"
run() {
  local wf=$1 job=$2 name=$3; shift 3
  echo "$name start $(date -Is)"
  HOMEDIR=$R/home-light "$O/run_job.sh" "$wf" "$job" "$name" "$@"
  echo "$name rc=$? end $(date -Is)"
}
run .github/workflows/rtl-fast.yml changes rf-changes
run .github/workflows/rtl-fast.yml verilator-lint rf-lint --needs changes.rtl=true
run .github/workflows/rtl-fast.yml bdd-conformance rf-bdd
run .github/workflows/rtl.yml full-ci-gate full-ci-gate
run .github/workflows/docs.yml wire-accountability wire-accountability
run .github/workflows/docs.yml docs-check-no-git docs-check-no-git
