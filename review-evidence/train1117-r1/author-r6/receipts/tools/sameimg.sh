#!/bin/bash
# sameimg.sh: arm A's images at 1x1/1if and 8x8/1if built at the p10 tip 25299527, against the measured febbfc4b builds'.
. <scratch>/bin/env.sh
T=<scratch>; export MAKEFLAGS="-j4 --no-print-directory"
for P in 1x1 8x8-1if; do
  python3 -B $T/tools/legs.py build $T/clones/r4-tip-img $T/r4meas/sameimg/$P $P none 1 aecp-largest-notice > $T/r4meas/sameimg/$P.log 2>&1
  a=$(sha256sum $T/r4meas/sameimg/$P/image/ctrl_app.elf | cut -c1-16); b=$(sha256sum $T/r4meas/febbfc4b/$P/none/image/ctrl_app.elf | cut -c1-16)
  g1=$(find $T/r4meas/sameimg/$P/gateware -name '*.v' -newer $T/r4meas/sameimg/$P.log -prune -o -name 'sim.v' -print | head -1)
  echo "$P: tip 25299527 ctrl_app.elf $a, measured febbfc4b $b: $([ $a = $b ] && echo identical || echo DIFFERENT)"
done
