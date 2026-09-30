#!/bin/sh
# Run each named round-4 reviewer probe (r413_plants.py) through gate 1b,
# early-stopped by the prior round's early_stop3.py and run by its
# run_gate1b.py (both copied unchanged under scripts/r412-3), on a disposable
# `git archive` copy of the clone (submodules at their gitlinks), at most 8
# jobs at once.  One log per probe: receipts/r413/gate1b_early_<probe>.log.
# usage: r413_probe.sh <clone> <packet> <probe>...
set -eu
clone=$1; packet=$2; shift 2
run_one() {
    probe=$1
    tree=$packet/scratch/trees/r413_$probe
    rm -rf "$tree"; mkdir -p "$tree"
    git -C "$clone" archive HEAD | tar -x -C "$tree"
    for sub in gptp-processor protocol-processor third_party/verilog-axis; do
        pin=$(git -C "$clone" rev-parse "HEAD:$sub")
        mkdir -p "$tree/$sub"
        git -C "$clone/$sub" archive "$pin" | tar -x -C "$tree/$sub"
    done
    log=$packet/receipts/r413/gate1b_early_$probe.log
    {
        echo "probe=$probe head=$(git -C "$clone" rev-parse HEAD)"
        python3 "$packet/scripts/r413_plants.py" "$tree" "$probe"
        set +e
        python3 "$packet/scripts/r412-3/early_stop3.py" "$tree"
        R412_EARLY=1 python3 "$packet/scripts/r412-3/run_gate1b.py" "$tree"
        echo "rc=$?"
    } > "$log" 2>&1
}
mkdir -p "$packet/receipts/r413"
for probe in "$@"; do
    while [ "$(jobs -r | wc -l)" -ge 8 ]; do sleep 2; done
    run_one "$probe" &
done
wait
