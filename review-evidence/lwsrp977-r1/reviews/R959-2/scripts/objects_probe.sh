#!/bin/bash
# objects_probe.sh <repo> <base-rev> <head-rev> <work> <cc...>
# Compile every C source under src/ of both revisions with each flag set and each
# compiler, from the same relative paths, and compare objects byte for byte.
# With -g, compare after objcopy --strip-debug. Prints one line per object.
set -u
repo=$1; base=$2; head=$3; work=$4; shift 4
compilers=("$@")
rm -rf "$work"; mkdir -p "$work"
for rev in base head; do
  sha=$([ $rev = base ] && echo "$base" || echo "$head")
  mkdir -p "$work/$rev"
  git -C "$repo" archive "$sha" src | tar -x -C "$work/$rev"
done
SOURCES=$(cd "$work/head" && find src -name '*.c' | sort)
same=0; total=0; fail=0
FLAGSETS=(
"O0|-O0" "O2|-O2" "Os|-Os"
"O0-milan|-O0 -DLWSRP_MILAN=1" "O2-milan|-O2 -DLWSRP_MILAN=1" "Os-milan|-Os -DLWSRP_MILAN=1"
"O2-fPIC|-O2 -fPIC" "O0-fPIC|-O0 -fPIC" "O1|-O1" "O3|-O3"
"g-O0|-g -O0" "g-O2|-g -O2" "g-Os-milan|-g -Os -DLWSRP_MILAN=1"
)
for ccx in "${compilers[@]}"; do
  for fs in "${FLAGSETS[@]}"; do
    label=${fs%%|*}; flags=${fs#*|}
    for s in $SOURCES; do
      for rev in base head; do
        o="$work/obj/$ccx/$label/$rev/${s//\//_}.o"; mkdir -p "$(dirname "$o")"
        if ! (cd "$work/$rev" && "$ccx" -std=c11 $flags -Isrc/include -Isrc -c "$s" -o "$o" 2>/dev/null); then
          echo "BUILD-FAIL $ccx $label $rev $s"; fail=$((fail + 1))
        fi
        case $label in g-*) objcopy --strip-debug "$o" "$o.s" && mv "$o.s" "$o" ;; esac
      done
      a="$work/obj/$ccx/$label/base/${s//\//_}.o"; b="$work/obj/$ccx/$label/head/${s//\//_}.o"
      total=$((total + 1))
      if cmp -s "$a" "$b"; then same=$((same + 1)); r=SAME; else r=DIFF; fi
      echo "$r $ccx $label $s $(sha256sum < "$a" | cut -c1-16) $(sha256sum < "$b" | cut -c1-16)"
    done
  done
done
echo "objects byte-identical: $same of $total, build failures $fail (base $base, head $head)"
[ "$same" -eq "$total" ] && [ "$fail" -eq 0 ]
