#!/bin/bash
# Focused MAAP bank on a scratch copy of the exact head. Usage: run_bank.sh <packet-dir>
# Each job writes receipts/<job>.log and receipts/<job>.rc.
P=$1; T=$P/scratch/repo/tb/verilator/maap; R=$P/receipts
export PATH=$P/scratch/bin:$PATH VERILATOR=$P/scratch/bin/verilator
job() { name=$1; shift; setsid nohup bash -c "cd $T && $* ; echo \$? > $R/$name.rc" > $R/$name.log 2>&1 < /dev/null & }
job integration "make -s integration-build DP_MDIR=$P/scratch/obj_integ VERILATOR_JOBS=4 && cd $P/scratch/obj_integ && ./maap_integration"
job campaign "VERILATOR_JOBS=4 python3 -I mutants.py"
