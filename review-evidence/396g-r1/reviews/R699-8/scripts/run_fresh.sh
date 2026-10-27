#!/bin/sh
# Run fresh_seeds.py over fresh and gate seed ranges, 16 jobs at a time, in the foreground.
# usage: run_fresh.sh <planner.py> <receipt-dir>
set -u
here=$(dirname "$0")
planner=$1
out=$2
mkdir -p "$out"
run() {
    n=$1_$2_$3_$4
    python3 -I -B "$here/fresh_seeds.py" "$planner" "$1" "$2" "$3" "$4" > "$out/$n.jsonl" 2> "$out/$n.err"
    echo $? > "$out/$n.rc"
}
for fam in arm nested; do
    for fr in 8192 16384; do
        for lo in 20000 21000 22000 23000; do
            run $fam $fr $lo $((lo + 1000)) &
        done
    done
done
wait
run arm 16384 0 288 &
run nested 8192 0 48 &
run nested 16384 0 48 &
wait
