#!/bin/sh
# Run the WHOLE gate 1b (the prior round's run_gate1b.py, unchanged) on a
# byte copy of the clone with one r413_census_mutants.py mutant planted, at
# most 8 at once; one log per mutant in receipts/r413/census_mutant_<name>.log.
# usage: r413_census_run.sh <clone> <packet> <mutant>...
set -eu
clone=$1; packet=$2; shift 2
run_one() {
    name=$1
    tree=$packet/scratch/trees/r413_mut_$name
    rm -rf "$tree"; mkdir -p "$tree"; cp -a "$clone/." "$tree/"
    log=$packet/receipts/r413/census_mutant_$name.log
    {
        echo "mutant=$name head=$(git -C "$clone" rev-parse HEAD)"
        python3 "$packet/scripts/r413_census_mutants.py" "$tree" "$name"
        set +e
        python3 "$packet/scripts/r412-3/run_gate1b.py" "$tree"
        echo "rc=$?"
    } > "$log" 2>&1
}
mkdir -p "$packet/receipts/r413"
for name in "$@"; do
    while [ "$(jobs -r | wc -l)" -ge 8 ]; do sleep 2; done
    run_one "$name" &
done
wait
