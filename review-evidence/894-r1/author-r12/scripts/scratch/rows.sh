#!/bin/bash
# Each named AECP campaign row alone (aecp_mutants.py --shard INDEX COUNT) on TREE, into OUT/<index>.
# usage: rows.sh TREE OUT COUNT INDEX...
set -u
L=$1 O=$2 N=$3; shift 3
for i in "$@"; do
  mkdir -p "$O/$i"
  python3 -B "$L/sw/firmware/ctrl/test/aecp_mutants.py" --output "$O/$i" --shard "$i" "$N" > "$O/$i.out" 2>&1
  echo "row $i rc=$? $(grep -E '^\[(ok|ESCAPED)\]' "$O/$i.out")"
done
