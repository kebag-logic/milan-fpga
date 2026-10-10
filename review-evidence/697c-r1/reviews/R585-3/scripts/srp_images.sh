#!/usr/bin/env bash
# Link every ctrl_srp_image.py composition (5 shapes x 1/2 interfaces x without SRP / SRP / AECP) at a
# checkout with the reviewer's stand-in runtime archives. Usage: srp_images.sh <checkout> <out> <rt-dir>
set -u
R=$1; O=$2; RT=$3
for s in endstation_ax7101_1x1_tdm8 endstation_ax7101_8x8 endstation_arty_4x4 endstation_arty_8ch endstation_arty_current; do
 for i in 1 2; do for m in nosrp srp aecp; do echo "$s $i $m"; done; done; done |
xargs -P 4 -L 1 bash -c '
 s=$0; i=$1; m=$2; extra=""; [ $m = nosrp ] && extra=--without-srp; [ $m = aecp ] && extra=--with-aecp
 d='"$O"'/$s-if$i-$m; mkdir -p $d
 ( cd '"$R"' && python3 -B sw/firmware/ctrl/test/ctrl_srp_image.py --config configs/$s.yaml --output $d --interfaces $i $extra \
   --libc '"$RT"'/libc.a --compiler-runtime '"$RT"'/libcrt.a ) > $d.log 2>&1; echo "$s if$i $m rc=$?"'
