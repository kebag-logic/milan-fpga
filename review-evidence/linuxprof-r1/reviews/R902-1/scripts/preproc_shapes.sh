#!/usr/bin/env bash
# Preprocess ctrl_loop.h (macro dump) at base and head for each FPGA config's generated shape header, with no shape
# header, and at MBX_N_IF 1 and 2 (by overriding the contract's define through a wrapper), and compare.
# Usage: preproc_shapes.sh <base-tree> <head-tree> <identity-outdir> <workdir>
set -u
base=$1; head=$2; ids=$3; w=$4; rm -rf "$w"; mkdir -p "$w"; differ=0; n=0
for nif in 1 2; do
  for shp in none $(ls "$ids"/head | grep -- '-own$'); do
    for tag in base head; do tree=$base; [ $tag = head ] && tree=$head
      inc=(); [ $shp != none ] && inc=(-include "$ids/head/$shp/srp_entity.h")
      mkdir -p "$w/$tag/mbx"; sed "s/^#define MBX_N_IF 1u/#define MBX_N_IF ${nif}u/" "$tree/sw/firmware/ctrl/mbx/mbx_contract.h" > "$w/$tag/mbx/mbx_contract.h"
      printf '#include "ctrl_loop.h"\n' > "$w/$tag/p.c"
      gcc -std=c11 -E -dM "${inc[@]}" -I"$w/$tag/mbx" -I"$tree/sw/firmware/ctrl/loop" -I"$tree/sw/firmware/ctrl/mbx" "$w/$tag/p.c" 2> "$w/$tag/err-$nif-$shp" | grep -E '^#define (CTRL_LOOP|MBX_N_IF)' | sort > "$w/$tag/dm-$nif-$shp"
      sed -i "s#$tree#<TREE>#g; s#$w/$tag#<W>#g" "$w/$tag/err-$nif-$shp"
    done
    n=$((n+1))
    if cmp -s "$w/base/dm-$nif-$shp" "$w/head/dm-$nif-$shp" && diff -q <(grep -v '^In file' "$w/base/err-$nif-$shp" | sed -E 's/ctrl_loop.h:[0-9]+:/ctrl_loop.h:L:/; s/^ *[0-9]+ \|/ L |/') <(grep -v '^In file' "$w/head/err-$nif-$shp" | sed -E 's/ctrl_loop.h:[0-9]+:/ctrl_loop.h:L:/; s/^ *[0-9]+ \|/ L |/') >/dev/null; then
      echo "SAME   if=$nif shape=$shp  macros=$(wc -l < "$w/head/dm-$nif-$shp") errors=$(grep -c 'error' "$w/head/err-$nif-$shp")"
    else differ=1; echo "DIFFER if=$nif shape=$shp"; fi
  done
done
echo "compared $n points; differ=$differ"; exit $differ
