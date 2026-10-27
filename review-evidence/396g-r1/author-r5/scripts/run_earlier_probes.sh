#!/usr/bin/env bash
# Run the reviewer's round-3 and round-2 probes, byte-identical to their manifest, against one planner.
# Usage: bash run_earlier_probes.sh <reviewer scripts dir> <tb/tools dir> <out dir>
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
run r3_arm_void_probe "$rev/r3_arm_void_probe.py" "$tools" "$rev" 8
run r3_cluster_probe "$rev/r3_cluster_probe.py" "$tools" "$rev" 8
run r3_classify "$rev/r3_classify.py" "$out/r3_cluster_probe.log"
run r3_detail "$rev/r3_detail.py" "$tools" "$rev"
run r3_probe "$rev/r3_probe.py" "$tools" 8
run arm_interaction_probe_r2 "$rev/arm_interaction_probe_r2.py" "$tools" "$rev"
run compound_probe_r2 "$rev/compound_probe_r2.py" "$tools" "$rev"
run edge_probe_r2 "$rev/edge_probe_r2.py" "$tools" "$rev"
run grader_probe_r2 "$rev/grader_probe_r2.py" "$tools"
run port_grader_probe_r2 "$rev/port/grader_probe_r2.py" "$tools"
run n07_probe "$rev/n07_probe.py" "$tools" "$rev"
run throughput_misuse_r2 "$rev/throughput_misuse_r2.py" "$tools" "$rev"
