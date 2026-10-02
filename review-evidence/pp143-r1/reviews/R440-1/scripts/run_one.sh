#!/bin/bash
# usage: run_one.sh TAG CPULIST CMD...   (run from anywhere; logs to receipts/runs)
. $REVIEWS/pp143-r440-1-packet/scripts/env.sh
tag=$1; cpus=$2; shift 2
mkdir -p $P/receipts/runs
out=$P/receipts/runs/$tag
{ echo "tag=$tag cpus=$cpus"; echo "cmd=$*"; echo "verilator=$(verilator --version)"; echo "start=$(date -u +%FT%TZ) $(date +%s)"; } > $out.meta
cd $SRC
start=$(date +%s)
taskset -c "$cpus" "$@" > $out.stdout 2> $out.stderr
rc=$?
end=$(date +%s)
echo "end=$(date -u +%FT%TZ) $end" >> $out.meta
echo "wall_s=$((end-start))" >> $out.meta
echo $rc > $out.rc
