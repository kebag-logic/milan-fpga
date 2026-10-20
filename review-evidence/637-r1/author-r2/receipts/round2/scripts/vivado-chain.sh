#!/usr/bin/env bash
# route-1x1, ooc-1x1, ooc-8x8 (round-1 drivers, recipe unchanged) and the xvlog gate at the round-2 head
S=<scratch>
R=$S/head3
date -u +%FT%TZ; git -C $R rev-parse HEAD
rc1=0; bash $S/scripts/route.sh r2 $R || rc1=$?
echo "ROUTE-SCRIPT rc=$rc1"; date -u +%FT%TZ
rc2=0; bash $S/scripts/ooc1x1.sh r2 $R > $S/route-r2/ooc1x1.log 2>&1 || rc2=$?
echo "OOC1X1-SCRIPT rc=$rc2"; date -u +%FT%TZ
rc3=0; bash $S/scripts/ooc8x8.sh r2 $R > $S/route-r2/ooc8x8.log 2>&1 || rc3=$?
echo "OOC8X8-SCRIPT rc=$rc3"; date -u +%FT%TZ
cd $R
export TMPDIR=$S/tmp
export PATH=<home>/Xilinx/2026.1/Vivado/bin:$S/venv312/bin:$PATH
rc4=0; flock -x $VIVADO_LOCK python3 scripts/xvlog_gate.py --check > $S/route-r2/xvlog-check.log 2>&1 || rc4=$?
echo "XVLOG rc=$rc4"
rc5=0; python3 scripts/xvlog_gate.py --selftest > $S/route-r2/xvlog-selftest.log 2>&1 || rc5=$?
echo "XVLOG-SELFTEST rc=$rc5"; date -u +%FT%TZ
echo CHAIN-DONE
