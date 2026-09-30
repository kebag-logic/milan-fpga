#!/bin/sh
# Run each named gate-1b probe on its own disposable copy of the exact head.
# usage: probe_all.sh <clone> <packet> <probe>...
# Each copy is `git archive HEAD` of the clone (plus each submodule at its
# gitlink) under <packet>/scratch/trees,
# planted by plants3.py, instrumented by early_stop3.py, and run through
# run_gate1b.py with R412_EARLY=1 (at most 8 jobs at once).  The log of each
# lands in <packet>/receipts/gate1b_<mode>_<probe>.log with the exit code.
# R412_MODE=full runs the WHOLE gate 1b uninstrumented (default: early).
set -eu
clone=$1; packet=$2; shift 2
scripts=$packet/scripts
run_one() {
    probe=$1
    tree=$packet/scratch/trees/$probe
    mode=${R412_MODE:-early}
    rm -rf "$tree"; mkdir -p "$tree"
    if [ "$mode" = full ]; then
        # the whole gate reads the submodules' git metadata: a byte copy of
        # the clone, repositories included (the clone itself is only read)
        cp -a "$clone/." "$tree/"
    else
        git -C "$clone" archive HEAD | tar -x -C "$tree"
        for sub in gptp-processor protocol-processor third_party/verilog-axis; do
            pin=$(git -C "$clone" rev-parse "HEAD:$sub")
            mkdir -p "$tree/$sub"
            git -C "$clone/$sub" archive "$pin" | tar -x -C "$tree/$sub"
        done
    fi
    log=$packet/receipts/gate1b_${mode}_$probe.log
    {
        echo "probe=$probe head=$(git -C "$clone" rev-parse HEAD)"
        python3 "$scripts/plants3.py" "$tree" "$probe"
        set +e
        if [ "$mode" = early ]; then
            python3 "$scripts/early_stop3.py" "$tree"
            R412_EARLY=1 python3 "$scripts/run_gate1b.py" "$tree"
        else
            python3 "$scripts/run_gate1b.py" "$tree"
        fi
        echo "rc=$?"
    } > "$log" 2>&1
}
for probe in "$@"; do
    while [ "$(jobs -r | wc -l)" -ge 8 ]; do sleep 2; done
    run_one "$probe" &
done
wait
