#!/bin/sh
# Emit every tracked configuration's builder artifacts at both placements from two exported trees and compare them.
# Usage: artifacts_compare.sh <base_tree> <head_tree> <outdir>
B=$1; H=$2; O=$3; mkdir -p "$O"
for t in base head; do
  T=$B; [ $t = head ] && T=$H
  for c in "$T"/configs/endstation_*.yaml; do
    n=$(basename "$c" .yaml)
    for p in all-fabric split; do
      (cd "$T" && python3 -B sw/builder/endstation_builder.py "$c" -o "$O/$t/$n-$p" --placement $p > "$O/$t-$n-$p.log" 2>&1; echo "$t $n $p rc=$?")
    done
  done
done
for d in "$O"/base/*; do n=$(basename "$d"); if diff -r -q "$d" "$O/head/$n" > "$O/diff-$n.txt" 2>&1; then echo "IDENTICAL $n"; else echo "DIFFERS $n ($(wc -l < "$O/diff-$n.txt") entries)"; fi; done
