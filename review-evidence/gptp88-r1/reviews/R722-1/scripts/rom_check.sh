#!/bin/sh
# rom_check.sh <repo> <outdir>: regenerate every image from base and head generators and compare
# with each other and with the tracked .hex blobs at head.
repo=$1; o=$2; mkdir -p "$o"
for rev in 55680bff3b287b9a7b0c759f51471fa617c17335 c1bc9e21a273fd8506b4806a2470fb7bab13f72f; do
  git -C "$repo" show "$rev:hdl/ucode/gen_gptp_ucode.py" > "$o/gen_$rev.py"
done
i=0
while IFS='|' read -r tag args; do
  for rev in 55680bff3b287b9a7b0c759f51471fa617c17335 c1bc9e21a273fd8506b4806a2470fb7bab13f72f; do
    python3 -I "$o/gen_$rev.py" $args -o "$o/$tag.$rev.hex" > "$o/$tag.$rev.genlog" 2>&1 || echo "GEN FAIL $tag $rev"
  done
  if cmp -s "$o/$tag.55680bff3b287b9a7b0c759f51471fa617c17335.hex" "$o/$tag.c1bc9e21a273fd8506b4806a2470fb7bab13f72f.hex"; then echo "IDENTICAL base-vs-head $tag ($args)"; else echo "DIFFER base-vs-head $tag ($args)"; fi
done <<'LIST'
default|
engine|--clk-hz 2000000 --cease-ms 3000
engine-seq|--clk-hz 2000000 --cease-ms 3000 --seq-seed 0x200000
engine-sync|--clk-hz 2000000 --cease-ms 3000 --sync-seq-seed 0x10000
engine-p1|--clk-hz 2000000 --cease-ms 3000 --p1 255
tsngen|--clk-hz 2000000
bench248|--p1 248
LIST
for pair in "tb/verilator/engine/gptp_ucode.hex engine" "tb/verilator/ucpu/gptp_ucode.hex default" "tb/tsngen/gptp_ucode.hex tsngen" "syn/ooc/work/gptp_ucode.hex default"; do
  set -- $pair
  git -C "$repo" show "c1bc9e21a273fd8506b4806a2470fb7bab13f72f:$1" > "$o/tracked.hex"
  if cmp -s "$o/tracked.hex" "$o/$2.c1bc9e21a273fd8506b4806a2470fb7bab13f72f.hex"; then echo "TRACKED-MATCH $1 == regenerated $2"; else echo "TRACKED-DIFF $1 vs regenerated $2"; fi
  b=$(git -C "$repo" rev-parse "55680bff3b287b9a7b0c759f51471fa617c17335:$1"); h=$(git -C "$repo" rev-parse "c1bc9e21a273fd8506b4806a2470fb7bab13f72f:$1"); echo "blob $1 base $b head $h"
done
