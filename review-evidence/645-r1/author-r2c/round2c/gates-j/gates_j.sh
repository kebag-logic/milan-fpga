#!/bin/bash
# Gates touched by the dev 09f1841b merge (886e1620): mbx suite, portability, firmware-unit job.
W=$VALIDATION_STORAGE/645-a531/round2c/functional
O=$W/gates-j
export PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 MAKEFLAGS=-j8 VERILATOR_JOBS=2 TMPDIR=$VALIDATION_STORAGE/645-a531/round2c/tmp
export VERILATOR=$W/run-simulator-limited PATH=$W/shims:$VALIDATION_TOOLS/pinned-verilator-5.050:$VALIDATION_STORAGE/231-a337-sdk/bin:$PATH
run() { n=$1; d=$2; shift 2; echo "$(date +%T) START $n" >> $O/driver.log; (cd $d && "$@") > $O/$n.log 2>&1; rc=$?; echo $rc > $O/$n.rc; echo "$(date +%T) DONE $n $rc" >> $O/driver.log; }
(
  run mbx $W/tree timeout 14400 make -C tb/verilator/mbx
  run mbx-verdict $W/tree python3 scripts/suite_tally.py --verdict $O/mbx.log
  run portability $W/tree bash syn/yosys/run.sh
) &
(
  sed -i "s#/firmware-unit-h#/gates-j/firmware#" $W/firmware_unit_j.sh 2>/dev/null
  mkdir -p $O/firmware && run firmware $W/builder bash $W/firmware_unit_j.sh
) &
wait
rc=0; for f in $O/*.rc; do [ "$(cat $f)" = 0 ] || rc=1; done; echo $rc > $O/all.rc
