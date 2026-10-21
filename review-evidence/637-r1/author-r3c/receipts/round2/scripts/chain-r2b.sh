#!/usr/bin/env bash
# ooc-8x8 (round-1 driver, recipe unchanged) and the xvlog gate at 887b6bf2 (hdl equal to the head), rerun after the host reset
S=<scratch>
R=$S/head3
date -u +%FT%TZ; git -C $R rev-parse HEAD
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
