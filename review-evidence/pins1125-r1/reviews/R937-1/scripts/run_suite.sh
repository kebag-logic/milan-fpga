#!/bin/sh
# usage: run_suite.sh <name> <cpus> <repo> <logdir> <command...>
# Runs one suite under a CPU fence, writing <logdir>/<name>.log and <name>.rc.
name=$1; cpus=$2; repo=$3; logdir=$4; shift 4
cd "$repo" || exit 99
start=$(date +%s)
taskset -c "$cpus" "$@" > "$logdir/$name.log" 2>&1
rc=$?
end=$(date +%s)
echo "$rc" > "$logdir/$name.rc"
echo "elapsed_s=$((end-start)) rc=$rc cmd=$*" > "$logdir/$name.meta"
