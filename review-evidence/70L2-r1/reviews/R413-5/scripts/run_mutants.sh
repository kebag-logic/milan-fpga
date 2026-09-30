#!/bin/sh
# Run gate 1b to the verdict-break stop on a byte copy of <clone> per mutant.
# usage: run_mutants.sh <clone> <packet> <mutant>...   (at most 6 at once)
set -eu
clone=$1; packet=$2; shift 2
run_one() {
    name=$1
    tree=$packet/scratch/trees/m_$name
    rm -rf "$tree"; mkdir -p "$tree"; cp -a "$clone/." "$tree/"
    log=$packet/receipts/mutants/m_$name.log
    {
        echo "mutant=$name head=$(git -C "$clone" rev-parse HEAD)"
        python3 -B "$packet/scripts/census_mutants.py" "$tree" "$name"
        python3 -B "$packet/scripts/plant_stop.py" "$tree"
        set +e
        timeout 500 python3 -B -u "$packet/scripts/run_profile_contract.py" "$tree"
        echo "rc=$?"
    } > "$log" 2>&1
    rm -rf "$tree"
}
mkdir -p "$packet/receipts/mutants" "$packet/scratch/trees"
for name in "$@"; do
    while [ "$(jobs -r | wc -l)" -ge 6 ]; do sleep 2; done
    run_one "$name" &
done
wait
