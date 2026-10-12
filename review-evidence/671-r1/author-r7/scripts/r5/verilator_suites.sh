#!/usr/bin/env bash
# The Verilator suites that read the writer firmware, run one after the other
# with the pinned Verilator 5.050, the pinned GNU make 4.3 and the scratch
# CPython 3.12.3 first on PATH, at most two Verilator build jobs.
# Usage: verilator_suites.sh <repo> <logdir>
set -u
repo=$1; logs=$2
export PATH="$VALIDATION_TOOLS/pinned-verilator-5.050:$VALIDATION_STORAGE/641-a573/make-4.3:$VALIDATION_STORAGE/671-a592/venv312/bin:$PATH"
export VERILATOR_JOBS=2 TMPDIR=$VALIDATION_STORAGE/671-a592/r5/tmp
cd "$repo" || exit 2
echo "START nvm_cosim $(date -Is) $(make --version | head -1) $(verilator --version)"
make -C tb/verilator/nvm_cosim run JOBS=2 POOL=4 > "$logs/nvm_cosim.log" 2>&1
echo "END nvm_cosim rc=$? $(date -Is)"
echo "START fw_service_budget $(date -Is)"
make -C tb/verilator/fw_service_budget > "$logs/fw_service_budget.log" 2>&1
echo "END fw_service_budget rc=$? $(date -Is)"
