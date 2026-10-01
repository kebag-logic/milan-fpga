#!/usr/bin/env bash
# Mutation probes on a disposable copy of the pinned packets: does each figures
# command's output change when one of its claimed inputs changes?
# usage: mutation_probe.sh <extracted review-evidence/b5-r1 at the pin, after step 1> <work-dir>
set -euo pipefail
src=$1 work=$2
[[ -e $work ]] && { echo "refusing: $work exists" >&2; exit 2; }

figures() {  # $1 = root; prints sha256 of both outputs
    local a b
    a=$(python3 "$1/author-r2/tools/b5_attrib.py" figures "$1/author" "$1/author-r2/receipts" 2>&1 | sha256sum | cut -c1-16)
    b=$(python3 "$1/author-r3/tools/b5_round3.py" figures "$1/author" "$1/author-r2/receipts" 2>&1 | sha256sum | cut -c1-16)
    echo "$a $b"
}

cp -a "$src" "$work"
base=$(figures "$work")
echo "baseline (attrib round3): $base"
echo "receipts (attrib round3): $(sha256sum < "$src/author-r2/receipts/attribution.txt" | cut -c1-16) $(sha256sum < "$src/author-r3/receipts/round3_figures.txt" | cut -c1-16)"

probe() {  # $1 = label, $2 = relative file, $3 = python mutation snippet reading/writing p
    rm -rf "$work"; cp -a "$src" "$work"
    python3 - "$work/$2" <<EOF
import sys, json
p = sys.argv[1]
$3
EOF
    local got; got=$(figures "$work")
    local a=${got% *} b=${got#* } ba=${base% *} bb=${base#* }
    echo "$1: attrib $([[ $a == "$ba" ]] && echo unchanged || echo CHANGED), round3 $([[ $b == "$bb" ]] && echo unchanged || echo CHANGED)"
}

probe "read record, one entry +1 us" author-r2/receipts/a-long-reads.u16 \
'b = bytearray(open(p, "rb").read()); b[2000] = (b[2000] + 1) % 256; open(p, "wb").write(b)'
probe "summary.json continuity.window_time +1 s" author/summary/a-long/summary.json \
'd = json.load(open(p)); w = d["continuity"]["window_time"]; w[1] = w[1] + 1; d["continuity"]["window_time"] = w; json.dump(d, open(p, "w"))'
probe "continuity-events.csv, one data row removed" author/summary/a-long/continuity-events.csv \
'l = open(p).read().splitlines(True); del l[100]; open(p, "w").writelines(l)'
probe "peer-descs-2.jsonl, last line removed" author/restore/peer-descs-2.jsonl \
'l = open(p).read().splitlines(True); open(p, "w").writelines(l[:-1])'
probe "events.jsonl (a-long), every line removed" author/runs/a-long/events.jsonl \
'open(p, "w").write("")'
probe "events.jsonl (a-long), file deleted" author/runs/a-long/events.jsonl \
'import os; os.remove(p)'
rm -rf "$work"
