#!/bin/sh
# One census mutant (r413_census_mutants.py) AND one probe (r413_plants.py)
# on a disposable archive copy, gate 1b early-stopped as in r413_probe.sh.
# usage: r413_mutant_probe.sh <clone> <packet> <mutant> <probe>
set -eu
clone=$1; packet=$2; mutant=$3; probe=$4
tree=$packet/scratch/trees/r413_mp_${mutant}_$probe
rm -rf "$tree"; mkdir -p "$tree"
git -C "$clone" archive HEAD | tar -x -C "$tree"
for sub in gptp-processor protocol-processor third_party/verilog-axis; do
    pin=$(git -C "$clone" rev-parse "HEAD:$sub")
    mkdir -p "$tree/$sub"
    git -C "$clone/$sub" archive "$pin" | tar -x -C "$tree/$sub"
done
mkdir -p "$packet/receipts/r413"
log=$packet/receipts/r413/mutant_probe_${mutant}_$probe.log
{
    echo "mutant=$mutant probe=$probe head=$(git -C "$clone" rev-parse HEAD)"
    python3 "$packet/scripts/r413_census_mutants.py" "$tree" "$mutant"
    python3 "$packet/scripts/r413_plants.py" "$tree" "$probe"
    set +e
    python3 "$packet/scripts/r412-3/early_stop3.py" "$tree"
    R412_EARLY=1 python3 "$packet/scripts/r412-3/run_gate1b.py" "$tree"
    echo "rc=$?"
} > "$log" 2>&1
