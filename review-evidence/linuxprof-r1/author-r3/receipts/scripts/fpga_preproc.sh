#!/usr/bin/env bash
# For every FPGA config's shape header (and none) at MBX_N_IF 1 and 2, compare between two trees:
# the full macro set ctrl_loop.h defines, the compiler's diagnostics (line numbers masked), and the
# object bytes of loop/ctrl_loop.c where it compiles. MBX_N_IF is set by force-including a contract
# variant ahead of the tree's (its include guard keeps the tree's out), as a two-interface arm does.
# usage: fpga_preproc.sh <base-tree> <head-tree> <work>
set -u
base=$1 head=$2 w=$3; mkdir -p "$w"; n=0 differ=0 objs=0
for cfg in "$head"/configs/endstation_*.yaml; do
  stem=$(basename "$cfg" .yaml)
  python3 -B "$head/sw/firmware/ctrl/srp/srp_entity.py" "$cfg" -o "$w/$stem.h" >/dev/null || { echo "generator failed $stem"; exit 2; }
done
for nif in 1 2; do
  for shp in none $(cd "$w" && ls endstation_*.h | sed 's/\.h$//'); do
    for tag in base head; do tree=$base; [ $tag = head ] && tree=$head; d="$w/$tag/$nif-$shp"; mkdir -p "$d"
      sed "s/^#define MBX_N_IF 1u$/#define MBX_N_IF ${nif}u/" "$tree/sw/firmware/ctrl/mbx/mbx_contract.h" > "$d/contract.h"
      inc=(-include "$d/contract.h"); [ "$shp" != none ] && inc+=(-include "$w/$shp.h")
      C=$tree/sw/firmware/ctrl
      flags=(-std=c11 -O2 -DNDEBUG -Wall -Wextra -Werror -pedantic "${inc[@]}" -I"$C/mbx" -I"$C/loop" -I"$C/port" -I"$C/app" -I"$C/aecp" -I"$C/srp" -I"$C/adp" -I"$C/acmp" -I"$C/maap" -I"$tree/third_party/tsn-c-stack/include" -I"$tree/third_party/lwSRP/src/include" -I"$tree/sw/firmware/ctrl_nvm")
      printf '#include "ctrl_loop.h"\n' | cc "${flags[@]}" -E -dM -x c - 2> "$d/err" | sort > "$d/macros"
      sed -i -E "s#$tree#<TREE>#g; s#$d#<D>#g; s/ctrl_loop.h:[0-9]+:[0-9]+:/ctrl_loop.h:L:/; s/^ *[0-9]+ \|/ L |/" "$d/err"
      grep -q 'error' "$d/err" || { cc "${flags[@]}" -c "$C/loop/ctrl_loop.c" -o "$d/ctrl_loop.o" 2>> "$d/err.o" || echo "cc failed" >> "$d/err.o"; }
    done
    n=$((n+1)); b="$w/base/$nif-$shp" h="$w/head/$nif-$shp"; verdict=SAME
    cmp -s "$b/macros" "$h/macros" || verdict=DIFFER
    diff -q <(grep -v '^In file' "$b/err") <(grep -v '^In file' "$h/err") >/dev/null || verdict=DIFFER
    if [ -f "$b/ctrl_loop.o" ] || [ -f "$h/ctrl_loop.o" ]; then cmp -s "$b/ctrl_loop.o" "$h/ctrl_loop.o" && objs=$((objs+1)) || verdict=DIFFER; obj="ctrl_loop.o identical"; else obj="refused by THE SHAPES"; fi
    [ $verdict = DIFFER ] && differ=1
    echo "$verdict if=$nif shape=$shp macros=$(wc -l < "$h/macros") MBX_N_IF=$(grep -E '^#define MBX_N_IF ' "$h/macros" | cut -d' ' -f3) host-guard-macro=$(grep -c CTRL_LOOP_HOST_H "$h/macros") $obj$(grep -q 'THE SHAPES' "$h/err" && echo ' (#error)')"
  done
done
echo "compared $n points; $objs ctrl_loop.o pairs byte-identical; differ=$differ"; exit $differ
