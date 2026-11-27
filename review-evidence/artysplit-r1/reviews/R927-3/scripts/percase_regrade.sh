#!/bin/bash
# Regrade every case of a census extract one at a time (receipt_regrade.py --case), JOBS in parallel.
# usage: percase_regrade.sh REGRADER EXTRACT OUTDIR JOBS
set -u
R=$1; E=$2; O=$3; J=$4
mkdir -p "$O"
python3 -I -c "import json,sys;[print(r['case']) for r in json.load(open(sys.argv[1]))['cases']]" "$E/census.json" > "$O/cases.txt"
export R E O
xargs -P "$J" -I{} bash -c 'n=$(echo {} | tr / _); cd /tmp && python3 -E -s "$R" "$E" --case {} > "$O/$n.log" 2>&1; echo $? > "$O/$n.rc"' < "$O/cases.txt"
pass=0; fail=0
while read -r c; do n=$(echo "$c" | tr / _); if [ "$(cat "$O/$n.rc")" = 0 ]; then pass=$((pass+1)); else fail=$((fail+1)); echo "FAIL $c: $(tail -n1 "$O/$n.log")"; fi; done < "$O/cases.txt"
echo "RESULT pass=$pass fail=$fail"
