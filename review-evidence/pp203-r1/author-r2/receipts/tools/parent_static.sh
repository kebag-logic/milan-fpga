#!/usr/bin/env bash
# run each parent static gate in the scratch parent; one log + rc per gate
set -u
P=<parent>; OUT=$1; shift
export PATH=<tool>:<tool>:<home>/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/bin:/bin
export VERILATOR=<tool>/verilator
export TSN_GEN_ROOT=<scratch>/tsn-gen
mkdir -p $OUT
i=0
while IFS= read -r cmd; do
  [ -z "$cmd" ] && continue
  i=$((i+1)); n=$(printf "%02d" $i)
  echo "$cmd" > $OUT/$n.cmd
  (cd $P && timeout 1800 bash -c "$cmd") < /dev/null > $OUT/$n.log 2>&1
  echo $? > $OUT/$n.rc
  echo "$n rc=$(cat $OUT/$n.rc) $cmd"
done
