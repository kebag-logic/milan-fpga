#!/bin/sh
# usage: run_probe.sh NAME CMD... ; writes NAME.log and NAME.rc under $OUT, run in $TREE
name=$1; shift
cd "$TREE" || exit 9
start=$(date +%s)
"$@" > "$OUT/$name.log" 2>&1
rc=$?
echo "rc=$rc seconds=$(( $(date +%s) - start ))" > "$OUT/$name.rc"
