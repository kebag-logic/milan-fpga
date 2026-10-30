#!/usr/bin/env bash
# parent_static.sh <out> <list>: run each parent static gate in the scratch parent; one cmd + log + rc per gate
set -u
P=<parent>; OUT=$1; LIST=$2
export PATH=<tool>/pinned-verilator-5.050:<tool>/sv2v-v0.0.12:<home>/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/bin:/bin
export VERILATOR=<tool>/pinned-verilator-5.050/verilator
export TSN_GEN_ROOT=<tsn-gen>
export TMPDIR=<parent-runs>/parent-tmp
mkdir -p $OUT
i=0
while IFS= read -r cmd; do
  [ -z "$cmd" ] && continue
  i=$((i+1)); n=$(printf "%02d" $i)
  echo "$cmd" > $OUT/$n.cmd
  (cd $P && timeout 1800 bash -c "$cmd") < /dev/null > $OUT/$n.log 2>&1
  echo $? > $OUT/$n.rc
  echo "$n rc=$(cat $OUT/$n.rc) $cmd"
done < $LIST
touch $OUT.done
