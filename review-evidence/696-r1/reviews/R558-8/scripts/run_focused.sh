#!/bin/bash
# Usage: run_focused.sh <clone> <packet>  -- starts the focused MAAP jobs detached,
# each with its own log and rc file under <packet>/receipts.
set -u
C=$1; P=$2; S=$P/scratch; R=$P/receipts
export PATH=$S/bin:$PATH VERILATOR=$S/bin/verilator TMPDIR=$S/tmp
mkdir -p $S/tmp
cd "$C/tb/verilator/maap"
job() { n=$1; shift; ( "$@" >"$R/$n.log" 2>&1; echo $? >"$R/$n.rc" ) & }
job unit       make -j16 run MDIR=$S/unit VERILATOR_JOBS=4
job integ      bash -c "make -j16 integration-build DP_MDIR=$S/integ VERILATOR_JOBS=4 && cd $S/integ && ./maap_integration"
job coverage   make -j16 coverage COV_MDIR=$S/cov VERILATOR_JOBS=4
job mutants    env VERILATOR_JOBS=4 python3 -I mutants.py
wait
