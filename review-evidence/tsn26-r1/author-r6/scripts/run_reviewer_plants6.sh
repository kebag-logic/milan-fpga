#!/bin/sh
# usage: run_reviewer_plants6.sh CLONE WORK OUT
# Runs both reviewers' round 5 plant scripts, unchanged, against the clone's HEAD (exported; the clone is never written).
set -u
C=$1; W=$2; O=$3
R=<reviews>
export TOOLS=<tools>
export TMPDIR=<scratch>/tmp
rm -rf "$W" "$O"; mkdir -p "$W" "$O"
(cd "$C" && git rev-parse HEAD) > "$O/head.txt"
sha256sum $R/tsn26-r793-5/scripts/run_reviewer_plants.sh $R/tsn26-r793-5/scripts/reviewer_plants.json $R/tsn26-r793-5/scripts/full_suite_killers.py $R/tsn26-r794-5/scripts/escape_check4.py $R/tsn26-r794-5/scripts/plants-r3.json > "$O/inputs.sha256"
sh $R/tsn26-r793-5/scripts/run_reviewer_plants.sh "$C" "$W/r793" > "$O/r793-reviewer-plants.txt" 2>&1; echo "rc $?" >> "$O/r793-reviewer-plants.txt"
mkdir -p "$W/tree"; (cd "$C" && git archive HEAD) | tar -x -C "$W/tree"
python3 -I $R/tsn26-r794-5/scripts/escape_check4.py "$W/tree" "$W/e4" "$O/r794-escape-check4.txt" $R/tsn26-r794-5/scripts/plants-r3.json > "$O/r794-escape-check4.log" 2>&1; echo "rc $?" >> "$O/r794-escape-check4.log"
echo done > "$O/done"
