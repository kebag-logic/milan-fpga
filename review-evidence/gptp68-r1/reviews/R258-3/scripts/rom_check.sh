#!/bin/sh
# SPDX-License-Identifier: CERN-OHL-W-2.0
# Regenerate the four tracked ROM images and the per-configuration images
# from an exported source tree, and compare each tracked image byte for byte
# with the committed one. Read-only against the tree it is given.
#
# usage: rom_check.sh <exported-tree> <out-dir>
set -eu
TREE=$1
OUT=$2
GEN="$TREE/hdl/ucode/gen_gptp_ucode.py"
mkdir -p "$OUT"
status=0

gen() { # name, args...
  name=$1; shift
  python3 "$GEN" "$@" -o "$OUT/$name.hex" >"$OUT/$name.log" 2>&1
}

gen engine --clk-hz 2000000 --cease-ms 3000
gen tsngen --clk-hz 2000000
gen ucpu
gen ooc
gen engine_seq --clk-hz 2000000 --cease-ms 3000 --seq-seed 0x200000
gen engine_sync --clk-hz 2000000 --cease-ms 3000 --sync-seq-seed 0x10000
for hz in 25000000 50000000 100000000 125000000; do
  gen "clk_$hz" --clk-hz "$hz"
done

cmp_one() { # generated, tracked
  if [ ! -f "$TREE/$2" ]; then
    echo "MISSING tracked $2"; status=1; return
  fi
  if cmp -s "$OUT/$1.hex" "$TREE/$2"; then
    echo "EQUAL   $2"
  else
    echo "DIFFER  $2"; status=1
  fi
}
cmp_one engine tb/verilator/engine/gptp_ucode.hex
cmp_one tsngen tb/tsngen/gptp_ucode.hex
cmp_one ucpu tb/verilator/ucpu/gptp_ucode.hex
cmp_one ooc syn/ooc/work/gptp_ucode.hex

(cd "$OUT" && sha256sum ./*.hex)
exit $status
