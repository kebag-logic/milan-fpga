#!/bin/sh
# Regenerate the four tracked microcode images of TREE from its own
# generator with each consumer's own arguments, and compare them to the
# tracked bytes. Usage: regen_images.sh TREE WORKDIR
set -eu
T=$(cd "$1" && pwd); W=$2; mkdir -p "$W"
G="$T/hdl/ucode/gen_gptp_ucode.py"
rc=0
chk() { # name args...
  n=$1; shift; tracked=$1; shift
  python3 -I "$G" "$@" -o "$W/$n.hex" >"$W/$n.gen.log" 2>&1 || { echo "GENFAIL $n"; rc=1; return; }
  a=$(sha256sum <"$W/$n.hex" | cut -d' ' -f1); b=$(sha256sum <"$T/$tracked" | cut -d' ' -f1)
  if [ "$a" = "$b" ]; then echo "MATCH $tracked $a"; else echo "DIFF $tracked regen=$a tracked=$b"; rc=1; fi
}
chk engine tb/verilator/engine/gptp_ucode.hex --clk-hz 2000000 --cease-ms 3000
chk tsngen tb/tsngen/gptp_ucode.hex --clk-hz 2000000
chk ucpu tb/verilator/ucpu/gptp_ucode.hex
chk ooc syn/ooc/work/gptp_ucode.hex
# word usage of shipping and seeded images, as the generator reports it
for v in "" "--seq-seed 0x200000" "--sync-seq-seed 0x10000" "--p1 255"; do
  echo "== usage $v"; python3 -I "$G" --clk-hz 2000000 --cease-ms 3000 $v -o "$W/u.hex" 2>&1 | tail -n 40
done
exit $rc
