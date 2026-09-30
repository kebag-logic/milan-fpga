#!/bin/sh
# Run gate 1b to the verdict-break stop on a byte copy of <clone> per probe.
# usage: run_probes.sh <clone> <packet> <probe>...   (at most 6 at once)
set -eu
clone=$1; packet=$2; shift 2
run_one() {
    name=$1
    tree=$packet/scratch/trees/p_$name
    rm -rf "$tree"; mkdir -p "$tree"; cp -a "$clone/." "$tree/"
    log=$packet/receipts/probes/p_$name.log
    {
        echo "probe=$name head=$(git -C "$clone" rev-parse HEAD)"
        python3 -B "$packet/scripts/limit_probes.py" "$tree" "$name"
        python3 -B "$packet/scripts/plant_stop.py" "$tree"
        set +e
        timeout 500 python3 -B -u "$packet/scripts/run_profile_contract.py" "$tree"
        echo "rc=$?"
    } > "$log" 2>&1
    rm -rf "$tree"
}
mkdir -p "$packet/receipts/probes" "$packet/scratch/trees"
for name in "$@"; do
    while [ "$(jobs -r | wc -l)" -ge 6 ]; do sleep 2; done
    run_one "$name" &
done
wait
