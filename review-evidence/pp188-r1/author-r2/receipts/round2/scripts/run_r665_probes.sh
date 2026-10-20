#!/usr/bin/env bash
# usage: run_r665_probes.sh <tree> <out dir>: the R665-1 probe script, data-only
# packet copy, at the given tree; rc and seconds to files beside the log.
set -u
. <scratch>/scripts/env.sh
tree=$1; out=$2
rm -rf "$out"; mkdir -p "$(dirname "$out")"
t0=$(date +%s)
python3 -I <scratch>/review-packets/R665-1/scripts/probes.py "$tree" "$out" --jobs 6 \
  --only U1-lo-not-owed U2-park-retires-on-txla U3-parked-applies-rx U5-csid-ignores-park \
         U6-retire-keeps-fourpack U7-same-ignores-rec-valid > "$out.log" 2>&1
echo $? > "$out.rc"
echo $(( $(date +%s) - t0 )) > "$out.sec"
