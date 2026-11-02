#!/usr/bin/env bash
# Scratch only: real Verilator builds of the suite in one clone, forever; stopped by killing its process group.
set -u
cd "$1" || exit 3
export MAKEFLAGS="-j2 --no-print-directory" VERILATOR_JOBS=2 VERILATOR=$VALIDATION_TOOLS/pinned-verilator-5.050/verilator PATH=$VALIDATION_TOOLS/pinned-verilator-5.050:$VALIDATION_STORAGE/scratch/a662/make43/bin:/usr/local/bin:/usr/bin:/bin TMPDIR=$VALIDATION_STORAGE/833-a726/tmp
while :; do
  git clean -qfdx -e gptp-processor -e third_party -e protocol-processor
  make -C tb/verilator/gptp_shadow run > /dev/null 2>&1
done
