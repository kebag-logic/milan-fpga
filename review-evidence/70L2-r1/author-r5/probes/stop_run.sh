#!/bin/sh
# Run gate 1b on a byte copy of the clone with one mutant planted by
# <mutant-script>, stopped right after its verdict controls by the round-4
# external review's r413_stop_after_breaks.py (R413_STOP=1) and run by the
# round-3 review's run_gate1b.py, both used unchanged from <review>. The same
# procedure as that review's r413_census_stop_run.sh, with this round's mutant
# scripts. One log per mutant: <packet>/receipts/stop_<name>.log, with the exit
# code; the copy is deleted after its run. At most 4 at once.
# usage: stop_run.sh <clone> <packet> <review> <mutant-script> <name>...
set -eu
clone=$1; packet=$2; review=$3; script=$4; shift 4
run_one() {
    name=$1
    tree=$packet/scratch/trees/stop_$name
    rm -rf "$tree"; mkdir -p "$tree"; cp -a "$clone/." "$tree/"
    log=$packet/receipts/stop_$name.log
    {
        echo "mutant=$name head=$(git -C "$clone" rev-parse HEAD)"
        python3 -B "$script" "$tree" "$name"
        python3 -B "$review/scripts/r413_stop_after_breaks.py" "$tree"
        set +e
        R413_STOP=1 python3 -B "$review/scripts/r412-3/run_gate1b.py" "$tree"
        echo "rc=$?"
    } > "$log" 2>&1
    rm -rf "$tree"
}
mkdir -p "$packet/receipts" "$packet/scratch/trees"
for name in "$@"; do
    while [ "$(jobs -r | wc -l)" -ge 4 ]; do sleep 2; done
    run_one "$name" &
done
wait
