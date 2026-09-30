#!/bin/sh
# Early-mode gate-1b probes of this round, the same procedure as the round-3
# review's probe_all.sh (git archive of the head plus each submodule at its
# gitlink, planted, instrumented by that review's early_stop3.py, run by its
# run_gate1b.py with R412_EARLY=1), with this round's plants_a460.py.
# usage: probe_a460.sh <clone> <packet> <probe>...   (at most 4 at once)
set -eu
clone=$1; packet=$2; shift 2
here=$(cd "$(dirname "$0")" && pwd)
run_one() {
    probe=$1
    tree=$packet/scratch/trees/a460_$probe
    rm -rf "$tree"; mkdir -p "$tree"
    git -C "$clone" archive HEAD | tar -x -C "$tree"
    for sub in gptp-processor protocol-processor third_party/verilog-axis; do
        pin=$(git -C "$clone" rev-parse "HEAD:$sub")
        mkdir -p "$tree/$sub"
        git -C "$clone/$sub" archive "$pin" | tar -x -C "$tree/$sub"
    done
    log=$packet/receipts/gate1b_early_a460_$probe.log
    {
        echo "probe=$probe head=$(git -C "$clone" rev-parse HEAD)"
        python3 "$here/plants_a460.py" "$tree" "$probe"
        set +e
        python3 "$packet/scripts/early_stop3.py" "$tree"
        R412_EARLY=1 python3 "$packet/scripts/run_gate1b.py" "$tree"
        echo "rc=$?"
    } > "$log" 2>&1
    rm -rf "$tree"
}
for probe in "$@"; do
    while [ "$(jobs -r | wc -l)" -ge 4 ]; do sleep 2; done
    run_one "$probe" &
done
wait
