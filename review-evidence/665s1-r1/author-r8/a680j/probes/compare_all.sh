#!/bin/bash
# Every comparison this round cites, into receipts/compare/, each headed by its reference and its sha256.
set -u
O=$MANAGEMENT/2026-09-23/665s1-a680j
M=$MANAGEMENT/2026-09-23
B=$VALIDATION_STORAGE/scratch/665s1-a680j-work/builds
I=$M/665s1-a680i/receipts/runs
S2F=$M/665s2-a681e/receipts/head-regrade
S2R=$M/665s2-a681c/receipts/runs
D=$O/receipts/compare
mkdir -p "$D"
cmp() {  # name prefix reference this-run what
  { echo "# $5"; echo; echo "reference: ${3#$M/} (sha256 $(sha256sum "$3" | cut -c1-16)...)"; echo "this run: ${4#$B/} (sha256 $(sha256sum "$4" | cut -c1-16)...)"; echo
    python3 -I "$O/probes/compare_rows.py" "$2" "$3" "$4"; } > "$D/$1.md"
}
mods() {  # name reference-json this-json what
  { echo "# $4"; echo; echo "reference: ${2#$M/}"; echo "this run: ${3#$B/}"; echo
    python3 -I "$O/probes/module_diff.py" "$2" "$3"; } > "$D/$1.txt"
}
cmp aecp-1x1-vs-s2 aecp "$S2F/A1/table.md" "$B/A1/results/table.md" "aecp group, arm A, 1x1: S2's final regrade beside this head"
cmp aecp-8x8-vs-s2 aecp "$S2F/A8/table.md" "$B/A8/results/table.md" "aecp group, arm A, 8x8: S2's final regrade beside this head"
cmp aecp-1x1-vs-probe1 aecp "$I/ack-1x1/results/table.md" "$B/A1/results/table.md" "aecp group, 1x1: the one-cycle acknowledgement probe of 27c54171 beside this head's bound acknowledgement"
cmp aecp-8x8-vs-probe1 aecp "$I/ack-8x8/results/table.md" "$B/A8/results/table.md" "aecp group, 8x8: the one-cycle acknowledgement probe of 27c54171 beside this head's bound acknowledgement"
cmp aecp-1x1-late256 aecp "$B/A1/results/table.md" "$B/probe-ack256-1x1/results/table.md" "aecp group, 1x1: this head beside the PROBE acknowledging at 256 bus cycles"
cmp aecp-1x1-late1024 aecp "$B/A1/results/table.md" "$B/probe-ack1024-1x1/results/table.md" "aecp group, 1x1: this head beside the PROBE acknowledging at 1024 bus cycles"
cmp fanout-B1-vs-s2 aecp_fanout "$S2F/B1/table.md" "$B/B1/results/table.md" "aecp-fanout group, arm B, 1x1: S2's final regrade beside this head"
cmp fanout-B8-vs-s2 aecp_fanout "$S2F/B8/table.md" "$B/B8/results/table.md" "aecp-fanout group, arm B, 8x8: S2's final regrade beside this head"
cmp fanout-A1-vs-s2 aecp_fanout "$S2F/A1/table.md" "$B/AF1/results/table.md" "aecp-fanout group, arm A, 1x1: S2's final regrade beside this head"
cmp fanout-A8-vs-s2 aecp_fanout "$S2F/A8/table.md" "$B/AF8/results/table.md" "aecp-fanout group, arm A, 8x8: S2's final regrade beside this head"
cmp s2-fanout-B1-first-vs-final aecp_fanout "$S2R/B1/table.md" "$S2F/B1/table.md" "S2's own first-round arm B 1x1 fan-out beside its final regrade (equal: its per-module record is comparable)"
cmp s2-fanout-B8-first-vs-final aecp_fanout "$S2R/B8/table.md" "$S2F/B8/table.md" "S2's own first-round arm B 8x8 fan-out beside its final regrade"
mods fanout-B1-modules "$S2R/B1/aecp-fanout.json" "$B/B1/results/aecp-fanout.json" "arm B 1x1 fan-out, each taking pass's top modules: S2 first round beside this head"
mods fanout-B8-modules "$S2R/B8/aecp-fanout.json" "$B/B8/results/aecp-fanout.json" "arm B 8x8 fan-out, each taking pass's top modules: S2 first round beside this head"
mods fanout-A1-modules "$S2R/A1/aecp-fanout.json" "$B/AF1/results/aecp-fanout.json" "arm A 1x1 fan-out, each taking pass's top modules: S2 first round beside this head"
mods fanout-A8-modules "$S2R/A8/aecp-fanout.json" "$B/AF8/results/aecp-fanout.json" "arm A 8x8 fan-out, each taking pass's top modules: S2 first round beside this head"
