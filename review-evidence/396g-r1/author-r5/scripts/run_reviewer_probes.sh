#!/usr/bin/env bash
# Run the reviewer's round-4 probes, byte-identical to their manifest, against one planner.
# Usage: bash run_reviewer_probes.sh <reviewer scripts dir> <tb/tools dir> <out dir>
set -u
rev=$1 tools=$2 out=$3
mkdir -p "$out"
run() {
    local name=$1
    shift
    python3 -I -B "$@" > "$out/$name.log" 2>&1
    echo $? > "$out/$name.rc"
    echo "$name rc=$(cat "$out/$name.rc") $(tail -1 "$out/$name.log" | cut -c1-150)"
}
run r4_net_sweep "$rev/r4_net_sweep.py" "$tools" "$rev" 8
run r4_regress_sweep "$rev/r4_regress_sweep.py" "$tools" "$rev" 8
run r4_cf_full "$rev/r4_cf_full.py" "$tools" "$rev"
run r4_arm_corruption_sweep "$rev/r4_arm_corruption_sweep.py" "$tools" "$rev" 8
run r4_checks "$rev/r4_checks.py" "$tools" "$rev"
run r4_detail "$rev/r4_detail.py" "$tools" "$rev"
run r4_a_detail "$rev/r4_a_detail.py" "$tools" "$rev"
run r4_r700_s1 "$rev/r4_r700_s1.py" "$tools" "$rev"
run r4_probe "$rev/r4_probe.py" "$tools" "$rev" 8
