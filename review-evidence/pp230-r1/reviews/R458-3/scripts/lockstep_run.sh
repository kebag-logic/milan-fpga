#!/usr/bin/env bash
# Rerun the published round-1 lockstep bench (base c4cb84ff KL_srp_top_ref vs a KL_srp_top under test).
# usage: lockstep_run.sh <tag> <hdl/srp under test> <cycles> <seeds> <shape>...   shape = name:M:N:AW:J:P:LV
set -u
S=$REVIEWS/pp230-r458-3-packet/scratch; L=$S/ls
tag=$1; dut=$2; cyc=$3; seeds=$4; shift 4
for sh in "$@"; do
  IFS=: read -r n m k aw j p lv <<< "$sh"
  o=$S/lsb/$tag-$n
  if ! $L/build.sh "$dut" "$o" $m $k $aw $j $p $lv >/dev/null 2>&1; then echo "$tag $n BUILD-FAIL"; tail -5 $o/build.log; continue; end=1; fi
  tot=0; tin=0
  for sd in $(seq 1 $seeds); do
    out=$($o/obj/Vlockstep $((500 + 7 * sd)) $cyc $((sd % 3)))
    echo "$tag $n seed=$((500 + 7 * sd)) :: $(echo "$out" | tail -1)"
    a=$(echo "$out" | sed -n 's/.*mismatch_cycles=\([0-9]*\) internal_mismatch_cycles=\([0-9]*\).*/\1 \2/p')
    set -- $a; tot=$((tot + ${1:-999999999})); tin=$((tin + ${2:-999999999}))
  done
  echo "SUMMARY $tag $n M=$m N=$k cycles=$cyc seeds=$seeds top_mismatch=$tot internal_mismatch=$tin"
  rm -rf $o/obj
done
