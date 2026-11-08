#!/bin/bash
# Run one tsn-c-stack gate command in the pinned environment, with its own log and rc file.
# usage: gates.sh RUN_DIR validate|baremetal
set -u
. $HOME/milan-fpga-management/2026-09-23/tsn27-a751/scripts/env.sh
R=$1 JOB=$2
mkdir -p "$R"
cd $LANES/tsn-c-stack-27-wire
case $JOB in
  validate) python3 scripts/validate.py --work "$R/build-validation" --jobs 16 --graphs > "$R/validate.log" 2>&1 ;;
  baremetal) python3 scripts/baremetal.py --work "$R/build-rv32" --jobs 16 > "$R/baremetal.log" 2>&1 ;;
  *) echo "unknown job $JOB"; exit 2 ;;
esac
echo $? > "$R/$JOB.rc"
