#!/usr/bin/env bash
# Compare the default build's objects at the head with the base's, source file
# by source file, under several flag sets (no debug info, so line shifts in
# comments cannot show). Usage: objects_identical.sh <base-tree> <head-tree> <work>
set -u
base=$1; head=$2; work=$3
mkdir -p "$work"
srcs="core/mrp_mad.c core/mrp_pdu.c core/switch.c modules/msrp.c modules/mvrp.c modules/mmrp.c ports/alloc.c ports/timer.c"
status=0
for flags in "-O2" "-Os" "-O0" "-O2 -DLWSRP_MILAN=1" "-Os -DLWSRP_MILAN=1" "-O2 -fPIC"; do
  tag=$(echo "$flags" | tr ' =' '__')
  for s in $srcs; do
    for side in base head; do
      root=$([ $side = base ] && echo "$base" || echo "$head")
      out="$work/$side-$tag-$(echo $s | tr / _).o"
      cc -std=c11 $flags -g0 -I"$root/src" -I"$root/src/include" -c "$root/src/$s" -o "$out" || { echo "BUILD FAIL $side $s $flags"; status=1; }
      objcopy --remove-section=.comment --remove-section=.note.GNU-stack --remove-section=.note.gnu.property "$out" "$out.s" 2>/dev/null
    done
    a="$work/base-$tag-$(echo $s | tr / _).o.s"; b="$work/head-$tag-$(echo $s | tr / _).o.s"
    if cmp -s "$a" "$b"; then echo "IDENTICAL [$flags] $s"; else echo "DIFFERENT [$flags] $s"; status=1; fi
  done
done
exit $status
