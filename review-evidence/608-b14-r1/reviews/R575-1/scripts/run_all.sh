#!/usr/bin/env bash
# Re-run every R575-1 recompute against the archived B14 packet and a checkout of the head.
# usage: run_all.sh <packet-root: .../review-evidence/608-b14-r1> <repo checkout at 6ec1a3a9> <out-dir>
set -euo pipefail
pk=$1 repo=$2 out=$3 here=$(cd "$(dirname "$0")" && pwd)
doc=$repo/docs/findings/B14_BENCH_5603C353.md
mkdir -p "$out"
python3 -I "$here/check_item2.py" "$pk" > "$out/item2_check.txt"
python3 "$here/check_item2_counters.py" "$pk" > "$out/item2_counters.txt"
python3 "$here/check_item3.py" "$pk" "$doc" > "$out/item3_check.txt"
python3 -I "$here/check_item4.py" "$pk" "$doc" > "$out/item4_check.txt"
python3 -I "$here/check_item4_headers.py" "$pk" > "$out/item4_headers.txt"
python3 -I "$here/check_soak.py" "$pk" > "$out/soak_check.txt"
python3 -I "$here/check_raw_index.py" "$pk" > "$out/raw_index_check.txt"
python3 -I "$here/check_findings.py" "$pk" "$repo" > "$out/findings_check.txt"
echo "all recomputes rc=0"
