#!/bin/bash
# usage: r849_launch.sh NAME CMD...  -- runs CMD in the clone, log and rc under receipts/runs
P=${R849_PACKET:-$(cd "$(dirname "$0")/.." && pwd)}; R=${R849_CLONE:?set R849_CLONE to a clean clone at the reviewed head}
name=$1; shift
. $P/scripts/r849_env.sh
cd $R
( start=$(date +%s); "$@" > $P/receipts/runs/$name.log 2>&1; rc=$?; end=$(date +%s)
  echo "$rc" > $P/receipts/runs/$name.rc; echo "wall_s=$((end-start))" >> $P/receipts/runs/$name.rc ) 
