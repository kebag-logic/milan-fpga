#!/bin/sh
# Run every docs.yml job on its own fresh clone of <head> through run_docs_yml.py:
# the three docs-gates jobs one after another, and the two light jobs beside them.
# The unit's memory is recorded each minute. usage: run_all_jobs.sh <head> <scratch root>
H=$1; R=$2; T=$(dirname "$0"); PY=$VALIDATION_STORAGE/797-a711g/gates/venv/bin/python3
mkdir -p "$R/logs"
cg=/sys/fs/cgroup$(cut -d: -f3 /proc/self/cgroup)
( while [ ! -e "$R/ALL_DONE" ]; do echo "$(date +%T) $(cat $cg/memory.current) $(cat $cg/memory.peak)" >> "$R/memory.txt"; sleep 60; done ) &
j() { "$PY" -B "$T/run_docs_yml.py" "$H" "$1" "$R" > "$R/logs/$1.runner.txt" 2>&1; echo $? > "$R/logs/$1.runner.rc"; }
( j docs-gates-0; j docs-gates-1; j docs-gates-2 ) & a=$!
( j wire-accountability; j docs-check-no-git ) & b=$!
# The run as recorded used `wait %2 %3; wait`, which in sh also waited on the
# memory loop above, so ALL_DONE was written by hand once every job was DONE.
wait $a $b
echo done > "$R/ALL_DONE"
