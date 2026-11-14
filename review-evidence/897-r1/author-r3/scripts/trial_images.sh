#!/bin/bash
# The images of the rehearsed second merge (scratch cl-trial: 25ea917f merged with #902's round-10 commit 7398ec0a,
# uncommitted) against 25ea917f's: the size fixture at the four points (fixtures3.sh) and the platform's by
# plat_ledger.py, each ELF's sha256 beside the composed head's own. usage: trial_images.sh
set -u
T=/data-2/milan/tmp/897-a776
. $T/scripts/env.sh
export TMPDIR=$T/r3/tmp/trial MAKEFLAGS="-j8 --no-print-directory"; mkdir -p $TMPDIR
B=$T/r3/builds/trial; rm -rf $B; mkdir -p $B
cd $T/r3/cl-trial
python3 -B tb/verilator/ctrl_split_boot/plat_ledger.py --build-dir $B/plat-ledger --self-test > $B/plat_ledger.log 2>&1; echo "plat_ledger rc=$?"
bash $T/scripts/r3/fixtures3.sh $PWD $B/plat-ledger $B/fixtures
for p in 1x1-if1 1x1-if2 8x8-if1 8x8-if2; do
  for k in "platform plat-ledger/$p" "fixture fixtures/fixture-$p"; do set -- $k
    a=$(sha256sum $T/r3/builds/boot-e45981f8/$2/ctrl_app.elf | cut -c1-16); b=$(sha256sum $B/$2/ctrl_app.elf | cut -c1-16)
    echo "$1 $p: e45981f8 $a trial $b $([ "$a" = "$b" ] && echo identical || echo DIFFER)"
  done
done
