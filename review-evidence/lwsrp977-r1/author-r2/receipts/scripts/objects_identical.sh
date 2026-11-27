#!/bin/bash
# objects_identical.sh <repo> <base-rev> <head-rev> <work>: compile every library source of both revisions with each
# flag set, without debug info, from the same relative paths, and compare the objects byte for byte.
set -u
repo=$1; base=$2; head=$3; work=$4
mkdir -p "$work"
for rev in base head; do
  sha=$([ $rev = base ] && echo "$base" || echo "$head")
  mkdir -p "$work/$rev"
  git -C "$repo" archive "$sha" src | tar -x -C "$work/$rev"
done
SOURCES="core/mrp_mad.c core/mrp_pdu.c core/switch.c ports/timer.c ports/alloc.c modules/msrp.c modules/mvrp.c modules/mmrp.c"
same=0; total=0
while IFS='|' read -r label flags; do
  for s in $SOURCES; do
    for rev in base head; do
      o="$work/obj/$label/$rev/${s//\//_}.o"; mkdir -p "$(dirname "$o")"
      (cd "$work/$rev" && cc -std=c11 $flags -Isrc/include -Isrc -c "src/$s" -o "$o") || echo "BUILD-FAIL $label $rev $s"
    done
    a="$work/obj/$label/base/${s//\//_}.o"; b="$work/obj/$label/head/${s//\//_}.o"
    total=$((total + 1))
    if cmp -s "$a" "$b"; then same=$((same + 1)); r=SAME; else r=DIFF; fi
    echo "$r $label $s $(sha256sum < "$a" | cut -c1-16) $(sha256sum < "$b" | cut -c1-16)"
  done
done <<'EOF'
O0|-O0
O2|-O2
Os|-Os
O0-milan|-O0 -DLWSRP_MILAN=1
O2-milan|-O2 -DLWSRP_MILAN=1
Os-milan|-Os -DLWSRP_MILAN=1
O2-fPIC|-O2 -fPIC
O0-fPIC|-O0 -fPIC
EOF
echo "objects byte-identical: $same of $total (base $base, head $head)"
[ "$same" -eq "$total" ]
