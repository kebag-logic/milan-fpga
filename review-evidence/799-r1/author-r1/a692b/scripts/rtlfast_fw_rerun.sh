#!/usr/bin/env bash
# #799: re-run the rtl-fast replica's six firmware jobs (and `changes`, which sets their scope) at <rev> in the same
# clone, after the first run's copied RV32 SDK failed the installer's provenance check. The SDK in RTLFAST_HOME is now
# a fresh `scripts/ci_rv32_sdk.py --archive` install from the pinned archive. As the hosted job, no MILAN_RV32_CC is
# set, so the tools take the verified SDK at $HOME/br-milan-rv32/host.
# usage: rtlfast_fw_rerun.sh <rev> [out-name]
set -u
rev=$1; name=${2:-run-fw2}; X=$VALIDATION_STORAGE/scratch/799-a692b; C=$X/clone-rtlfast-${rev:0:8}; O=$X/r/rtlfast-${rev:0:8}
D=$(cd "$(dirname "$0")" && pwd)
source "$D/env.sh"; source "$D/fw_env.sh"
unset MILAN_RV32_CC
export RTLFAST_HOME=$X/home-rtlfast VERILATOR_JOBS=4
s=$(date +%s)
$VALIDATION_STORAGE/scratch/a662/ci312/bin/python3 "$D/rtl_fast_steps.py" "$O/$name" "$C" "$rev" changes firmware-unit \
  firmware-control-mutants firmware-aecp-mutants firmware-srp-mutants firmware-boundary firmware-verilator \
  > "$O/$name.out" 2>&1; rc=$?
echo "$rc $(( $(date +%s)-s ))s rtl_fast_steps firmware jobs" > "$O/table-$name.txt"
echo RTLFAST-FW-DONE >> "$O/table-$name.txt"
