#!/usr/bin/env bash
# [R558] R558-7: focused MAAP runs at the exact head, each with its own log and rc.
# usage: run_focused.sh <clone> <packet>
C=$1; P=$2; S=$P/scratch
export VERILATOR=$VALIDATION_TOOLS/pinned-verilator-5.050/verilator TMPDIR=$S/tmp
VC=${VERILATOR_COVERAGE_DIR:?set to the bin directory holding the pinned 5.050 verilator_coverage}
cd "$C" || exit 9
( make -j8 -C tb/verilator/maap run MDIR=$S/unit VERILATOR=$VERILATOR VERILATOR_JOBS=4 > $P/receipts/unit.log 2>&1; echo $? > $P/receipts/unit.rc ) &
( make -j8 -C tb/verilator/maap integration-build DP_MDIR=$S/integration VERILATOR=$VERILATOR VERILATOR_JOBS=4 > $P/receipts/integration_build.log 2>&1; r=$?
  if [ $r = 0 ]; then (cd $S/integration && ./maap_integration) > $P/receipts/integration_run.log 2>&1; r=$?; fi; echo $r > $P/receipts/integration.rc ) &
( PATH=$VC:$PATH make -j8 -C tb/verilator/maap coverage COV_MDIR=$S/coverage VERILATOR=$VERILATOR VERILATOR_JOBS=2 > $P/receipts/coverage.log 2>&1; echo $? > $P/receipts/coverage.rc ) &
( cd tb/verilator/maap && VERILATOR_JOBS=4 python3 mutants.py > $P/receipts/mutants.log 2>&1; echo $? > $P/receipts/mutants.rc ) &
wait
echo done > $P/receipts/focused.done
