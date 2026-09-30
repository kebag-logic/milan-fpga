#!/bin/sh
# Run the WHOLE gate 1b on a byte copy of the clone with one premise mutant
# planted (premise_mutants.py), the procedure of the round-3 review's
# census_mutants_run.sh with that review's run_gate1b.py; log per mutant in
# <packet>/receipts/premise_mutant_<name>.log with the exit code.
# usage: premise_mutants_run.sh <clone> <packet> <mutant>...
set -eu
clone=$1; packet=$2; shift 2
here=$(cd "$(dirname "$0")" && pwd)
run_one() {
    name=$1
    tree=$packet/scratch/trees/premise_$name
    rm -rf "$tree"; mkdir -p "$tree"; cp -a "$clone/." "$tree/"
    log=$packet/receipts/premise_mutant_$name.log
    {
        echo "mutant=$name head=$(git -C "$clone" rev-parse HEAD)"
        python3 "$here/premise_mutants.py" "$tree" "$name"
        set +e
        python3 "$packet/scripts/run_gate1b.py" "$tree"
        echo "rc=$?"
    } > "$log" 2>&1
    rm -rf "$tree"
}
for name in "$@"; do
    run_one "$name" &
done
wait
