#!/usr/bin/env bash
# fw_preproc_all.sh <base-tree> <head-tree> <work>: for every FPGA config's SRP shape header (and none) at MBX_N_IF 1
# and 2, preprocess (-E -P, no line markers) every firmware .c under sw/firmware/ctrl outside test/ and host/ in both
# trees, and compare the token streams and diagnostics; where loop/ctrl_loop.c preprocesses cleanly also compare its
# -O2 object. A config point also gets its aecp_entity_gen.h; sources needing nvm_shape_gen.h stop at
# that include in both trees, and only their diagnostics are compared. MBX_N_IF is set by force-including a contract copy ahead of the tree's.
set -u
base=$1 head=$2 w=$3; rm -rf "$w"; mkdir -p "$w/sh"; points=0 same=0 files=0 clean=0 objs=0
for cfg in "$head"/configs/endstation_*.yaml; do
  stem=$(basename "$cfg" .yaml)
  python3 -B "$head/sw/firmware/ctrl/srp/srp_entity.py" "$cfg" -o "$w/sh/$stem.h" >/dev/null || { echo "generator failed $stem"; exit 2; }
  python3 -B "$base/sw/firmware/ctrl/srp/srp_entity.py" "$cfg" -o "$w/sh/$stem.base.h" >/dev/null
  mkdir -p "$w/gen/$stem"; python3 -B "$head/sw/firmware/ctrl/aecp/aecp_entity.py" "$cfg" -o "$w/gen/$stem/aecp_entity_gen.h" >/dev/null || { echo "aecp generator failed $stem"; exit 2; }
  cmp -s "$w/sh/$stem.h" "$w/sh/$stem.base.h" || { echo "srp_entity header differs base/head for $stem"; exit 2; }
done
srcs=$(cd "$head/sw/firmware/ctrl" && find . -name '*.c' -not -path './test/*' -not -path './host/*' | sort)
for nif in 1 2; do
  for shp in none $(cd "$w/sh" && ls endstation_*.h | grep -v '\.base\.h$' | sed 's/\.h$//'); do
    points=$((points+1)); pd=0
    for tag in base head; do tree=$base; [ $tag = head ] && tree=$head; d="$w/$tag/$nif-$shp"; mkdir -p "$d"
      sed "s/^#define MBX_N_IF 1u$/#define MBX_N_IF ${nif}u/" "$tree/sw/firmware/ctrl/mbx/mbx_contract.h" > "$w/$tag/contract$nif.h"
      inc=(-include "$w/$tag/contract$nif.h"); [ "$shp" != none ] && inc+=(-include "$w/sh/$shp.h" -I"$w/gen/$shp")
      C=$tree/sw/firmware/ctrl
      fl=(-std=c11 -O2 -DNDEBUG -pedantic "${inc[@]}" -I"$C/mbx" -I"$C/loop" -I"$C/port" -I"$C/app" -I"$C/aecp" -I"$C/srp" -I"$C/adp" -I"$C/acmp" -I"$C/maap" -I"$C/plat" -I"$C/nvm" -I"$tree/third_party/tsn-c-stack/include" -I"$tree/third_party/lwSRP/src/include" -I"$tree/sw/firmware/ctrl_nvm")
      for s in $srcs; do o="$d/$(echo $s | tr / _).i"; cc "${fl[@]}" -E -P "$C/$s" -o "$o" 2> "$o.err"
        sed -i -E "s#$tree#<TREE>#g; s#$w#<W>#g; s/:[0-9]+:[0-9]+:/:L:/; s/^ *[0-9]+ \|/ L |/" "$o.err"; done
      grep -q . "$d/._loop_ctrl_loop.c.i.err" 2>/dev/null || [ ! -s "$d/._loop_ctrl_loop.c.i" ] || cc "${fl[@]}" -c "$C/loop/ctrl_loop.c" -o "$d/ctrl_loop.o" 2>/dev/null
    done
    b="$w/base/$nif-$shp" h="$w/head/$nif-$shp"; nclean=0
    for s in $srcs; do f="$(echo $s | tr / _).i"; files=$((files+1))
      { [ ! -e "$b/$f" ] && [ ! -e "$h/$f" ] || cmp -s "$b/$f" "$h/$f"; } && diff -q <(grep -v '^In file\|^ *from' "$b/$f.err") <(grep -v '^In file\|^ *from' "$h/$f.err") >/dev/null || { pd=1; echo "  DIFFER $nif-$shp $s"; }
      [ -s "$h/$f.err" ] || nclean=$((nclean+1)); done
    obj=none; if [ -f "$b/ctrl_loop.o" ] || [ -f "$h/ctrl_loop.o" ]; then cmp -s "$b/ctrl_loop.o" "$h/ctrl_loop.o" && { obj=identical; objs=$((objs+1)); } || { obj=DIFFER; pd=1; }; fi
    [ $pd = 0 ] && same=$((same+1))
    echo "$([ $pd = 0 ] && echo SAME || echo DIFFER) if=$nif shape=$shp sources=$(echo $srcs | wc -w) preprocessed-clean=$nclean ctrl_loop.o=$obj shapes-error=$(grep -l "THE SHAPES" $h/.*.err 2>/dev/null | wc -l)"
  done
done
echo "points=$points same=$same file-pairs=$files ctrl_loop.o-identical=$objs"; [ $same = $points ]
