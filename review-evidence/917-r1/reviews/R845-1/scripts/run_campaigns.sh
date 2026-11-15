#!/bin/sh
# Usage: run_campaigns.sh <clone> <packet>  -- starts the bench, firmware and mutant campaigns, each with log + rc.
set -u
C=$1; P=$2; R=$P/receipts; S=$P/scratch
V=$VALIDATION_TOOLS/pinned-verilator-5.050/verilator
export VERILATOR=$V TMPDIR=$S/tmp
mkdir -p $R $S/tmp $S/fw
( cd $C/tb/verilator/mbx && make VERILATOR=$V VBUILD_JOBS=4 run-wb run-axil run-cosim run-if2 > $R/mbx_make.log 2>&1; echo $? > $R/mbx_make.rc ) &
( cd $C && python3 -B sw/firmware/ctrl/test/test_ctrl_firmware.py --jobs 4 --build-dir $S/fw > $R/ctrl_firmware.log 2>&1; echo $? > $R/ctrl_firmware.rc ) &
( cd $C/tb/verilator/mbx && python3 -B mutants.py --jobs 2 > $R/mbx_mutants_full.log 2>&1; echo $? > $R/mbx_mutants_full.rc ) &
wait
