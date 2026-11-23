#!/bin/sh
# Rebuild the linkreset leg's two models at the reviewed head and run its four arms,
# plus a refused arm under the planted link-up reset (word 13), each shape.
# usage: linkreset_probe.sh <clone at the head> <verilator> <receipt dir>
set -eu
CLONE=$1; VERILATOR=$2; OUT=$3
mkdir -p "$OUT"
cd "$CLONE/tb/verilator/milan_dp"
make -j16 VERILATOR="$VERILATOR" VERILATOR_JOBS=8 build-linkreset-1x1 build-linkreset-8x8 > "$OUT/../scratch/build.log" 2>&1
W=$(python3 -B ../../../sw/litex/mac_link_status.py gmii 1 | cut -d' ' -f2)
echo "word reset $W" > "$OUT/linkreset-word.txt"
for s in 1x1 8x8; do
  (./obj_linkreset_$s/Vmilan_dp_linkreset --word-reset "$W" --publish-ms 1500 --window-ms 1600 > "$OUT/linkreset-$s-published.txt" 2>&1; echo "rc $?" >> "$OUT/linkreset-$s-published.txt") &
  (./obj_linkreset_$s/Vmilan_dp_linkreset --word-reset "$W" --publish-ms 0 --window-ms 1600 > "$OUT/linkreset-$s-refused.txt" 2>&1; echo "rc $?" >> "$OUT/linkreset-$s-refused.txt") &
  (./obj_linkreset_$s/Vmilan_dp_linkreset --word-reset 13 --publish-ms 0 --window-ms 1600 > "$OUT/probe-refused-planted-$s.txt" 2>&1; echo "rc $?" >> "$OUT/probe-refused-planted-$s.txt") &
done
wait
# restore the clone: remove what the build generated
rm -rf obj_linkreset_1x1 obj_linkreset_8x8 ltn_rom.hex ucode.hex
