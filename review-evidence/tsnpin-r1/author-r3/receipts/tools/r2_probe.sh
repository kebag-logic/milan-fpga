#!/usr/bin/env bash
# r2_probe.sh: round 1's head on the pinned SDK, and a scratch variant of the redelivery without the loop's counts.
set -u
export HOME=<scratch>/sdk/home
D=<scratch>; R=$D/ledger3/runtime
cd $D
tools/snap.sh $D/snaps/r1head 50e2a722ef2671b3f5b017f97b1c7d41705c4f32 >/dev/null || exit 4
tools/ledger.sh $D/snaps/r1head $D/ledger3/r1head $R
tools/snap.sh $D/snaps/v1 $(git -C $D/snaps/sb2 rev-parse HEAD) >/dev/null || exit 5
python3 - <<'PY'
from pathlib import Path
p = Path('<scratch>/snaps/v1/sw/firmware/ctrl/acmp/acmp_mbx.c'); s = p.read_text()
a = "\t\tif (st != MBX_STATUS_OK) {\n\t\t\tl->stats.rx_bad += st == MBX_STATUS_BAD;\n\t\t\treturn;\n\t\t}\n\t\tl->stats.rx_records++;\n"
b = "\t\tif (st != MBX_STATUS_OK) {\n\t\t\treturn;\n\t\t}\n"
assert s.count(a) == 1; p.write_text(s.replace(a, b))
PY
tools/ledger.sh $D/snaps/v1 $D/ledger3/v1 $R
for s in 1x1 8x8; do
  X=$D/s2/base-$s/split-soc; shape=endstation_ax7101_$s; [ $s = 1x1 ] && shape=endstation_ax7101_1x1_tdm8
  tools/plat_ledger.sh $D/snaps/r1head $D/plat3/r1head $R $shape 1 $X/mapped/soc/csr.csv $X/flash-map
  led=; [ $s = 8x8 ] && led=platform-8x8-two-interfaces
  tools/plat_ledger.sh $D/snaps/r1head $D/plat3/r1head $R $shape 2 $X/mapped/soc/csr.csv $X/flash-map $led
done
