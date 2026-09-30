#!/bin/sh
# As r413_census_run.sh, but gate 1b stops right after its verdict controls
# (r413_stop_after_breaks.py, R413_STOP=1). Also runs the unmutated head
# ("none") the same way as the reference. Logs in
# receipts/r413/census_stop_<name>.log.  At most 8 jobs at once.
# usage: r413_census_stop_run.sh <clone> <packet> <mutant|none>...
set -eu
clone=$1; packet=$2; shift 2
run_one() {
    name=$1
    tree=$packet/scratch/trees/r413_stop_$name
    rm -rf "$tree"; mkdir -p "$tree"; cp -a "$clone/." "$tree/"
    log=$packet/receipts/r413/census_stop_$name.log
    {
        echo "mutant=$name head=$(git -C "$clone" rev-parse HEAD)"
        [ "$name" = none ] || python3 "$packet/scripts/r413_census_mutants.py" "$tree" "$name"
        python3 "$packet/scripts/r413_stop_after_breaks.py" "$tree"
        set +e
        R413_STOP=1 python3 "$packet/scripts/r412-3/run_gate1b.py" "$tree"
        echo "rc=$?"
    } > "$log" 2>&1
}
mkdir -p "$packet/receipts/r413"
for name in "$@"; do
    while [ "$(jobs -r | wc -l)" -ge 8 ]; do sleep 2; done
    run_one "$name" &
done
wait
