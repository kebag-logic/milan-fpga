#!/bin/sh
# Run the WHOLE gate 1b on a byte copy of the clone with one census mutant
# planted (census_mutants.py), at most 8 at once; log per mutant in
# <packet>/receipts/census_mutant_<name>.log with the exit code.
# usage: census_mutants_run.sh <clone> <packet> <mutant>...
set -eu
clone=$1; packet=$2; shift 2
run_one() {
    name=$1
    tree=$packet/scratch/trees/mut_$name
    rm -rf "$tree"; mkdir -p "$tree"; cp -a "$clone/." "$tree/"
    log=$packet/receipts/census_mutant_$name.log
    {
        echo "mutant=$name head=$(git -C "$clone" rev-parse HEAD)"
        python3 "$packet/scripts/census_mutants.py" "$tree" "$name"
        set +e
        python3 "$packet/scripts/run_gate1b.py" "$tree"
        echo "rc=$?"
    } > "$log" 2>&1
}
for name in "$@"; do
    while [ "$(jobs -r | wc -l)" -ge 8 ]; do sleep 2; done
    run_one "$name" &
done
wait
