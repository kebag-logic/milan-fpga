#!/bin/bash
# Focused parent consumer run: kebag-logic/milan-fpga tb/verilator/gptp_plane
# at a given parent revision, with the gptp-processor population replaced by
# an export of one donor revision. Only the files that suite reads are
# fetched (each checked against the parent tree's blob id); no parent
# checkout is created or edited.
# Usage: parent_gptp_plane.sh <donor clone> <donor rev> <parent rev> <workdir> <receipt>
set -euo pipefail
clone=$1; drev=$2; prev=$3; work=$4; receipt=$5
rm -rf "$work"; mkdir -p "$work"; cd "$work"
files="tb/verilator/gptp_plane/Makefile tb/verilator/gptp_plane/gptp_plane_wrap.sv
tb/verilator/gptp_plane/sim_main.cpp hdl/ieee8021as/ptp_timestamp/timestamp_counter.sv
tb/common/verilator_harness.hpp tb/common/gptp_tx_flags.hpp"
gh api "repos/kebag-logic/milan-fpga/git/trees/$prev?recursive=1" \
  --jq '.tree[] | "\(.sha) \(.path)"' > parent-tree.txt
{
  echo "# parent gptp_plane at $prev, gptp-processor = export of $(git -C "$clone" rev-parse "$drev"), $(date -u +%FT%TZ)"
  echo "# simulator: $(verilator --version) at $(command -v verilator)"
} > "$receipt"
for f in $files; do
  mkdir -p "$(dirname "$f")"
  gh api "repos/kebag-logic/milan-fpga/contents/$f?ref=$prev" \
    -H 'Accept: application/vnd.github.raw' > "$f"
  want=$(awk -v p="$f" '$2 == p {print $1}' parent-tree.txt)
  got=$(git hash-object "$f")
  [ "$want" = "$got" ] || { echo "blob mismatch $f" >> "$receipt"; exit 2; }
  echo "# $f blob $got (matches parent tree)" >> "$receipt"
done
mkdir -p gptp-processor
git -C "$clone" archive "$drev" | tar -x -C gptp-processor
cd tb/verilator/gptp_plane
set +e; make run >> "$receipt" 2>&1; rc=$?; set -e
echo "# exit: $rc" >> "$receipt"
grep -E 'checks:|^FAIL|^# exit' "$receipt"
