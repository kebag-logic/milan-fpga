#!/bin/bash
# ledger.sh CLONE OUT: the ROM ledger at a head: plat_ledger.py --self-test (the platform image at its four points and
# its controls) into OUT/pl, then the harness's 8x8/2if build of the size fixture in every arm into OUT/fx, and the
# memory test.
. <scratch>/bin/env.sh
export MAKEFLAGS=-j4 PYTHONUNBUFFERED=1
C=$1 O=$2; mkdir -p $O/pl $O/fx
cd $C && echo "HEAD $(git rev-parse --short=8 HEAD) start $(date +%T)"
python3 -B tb/verilator/ctrl_split_boot/plat_ledger.py --build-dir $O/pl --self-test > $O/plat-ledger.log 2>&1; echo "plat_ledger rc=$?"
for v in none answering-ports shutdown-entry answering-later answering-every-port valid-destinations; do
  python3 -B <scratch>/tools/legs.py build $C $O/fx/$v 8x8 $v 1 > $O/fx/$v.log 2>&1 &
done; wait; echo "fixture builds done"
<home>/litex-milan/venv/bin/python3 sw/litex/test_ctrl_memory.py > $O/ctrl_memory.log 2>&1; echo "ctrl_memory rc=$?"
echo "END $(date +%T)"
