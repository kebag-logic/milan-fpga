#!/bin/bash
# Focused parent consumer probe: kebag-logic/milan-fpga tb/verilator/gptp_shadow
# (real KL_gptp_txret envelope) at a given parent revision, gptp-processor
# replaced by an export of one donor revision, verilog-axis at the parent's
# pin, and an optional report-only probe patch applied to the copy. Only the
# files the suite reads are fetched, each checked against its tree's blob id.
# No parent checkout is created or edited.
# Usage: parent_gptp_shadow_probe.sh <donor clone> <donor rev> <parent rev> <workdir> <receipt> [patch]
set -euo pipefail
clone=$1; drev=$2; prev=$3; work=$4; receipt=$5; patch=${6:-}
rm -rf "$work"; mkdir -p "$work"; cd "$work"
gh api "repos/kebag-logic/milan-fpga/git/trees/$prev?recursive=1" \
  --jq '.tree[] | "\(.sha) \(.path)"' > parent-tree.txt
axis_pin=$(awk '$2 == "third_party/verilog-axis" {print $1}' parent-tree.txt)
gh api "repos/alexforencich/verilog-axis/git/trees/$axis_pin?recursive=1" \
  --jq '.tree[] | "\(.sha) \(.path)"' > axis-tree.txt
{
  echo "# parent gptp_shadow at $prev, gptp-processor = export of $(git -C "$clone" rev-parse "$drev"), verilog-axis $axis_pin, $(date -u +%FT%TZ)"
  echo "# simulator: $(verilator --version) at $(command -v verilator)"
  echo "# probe patch: ${patch:-none} $( [ -n "$patch" ] && sha256sum "$patch" | cut -d' ' -f1)"
} > "$receipt"
fetch() { # <repo> <ref> <path> <tree file> <dest>
  mkdir -p "$(dirname "$5")"
  gh api "repos/$1/contents/$3?ref=$2" -H 'Accept: application/vnd.github.raw' > "$5"
  want=$(awk -v p="$3" '$2 == p {print $1}' "$4")
  got=$(git hash-object "$5")
  [ -n "$want" ] && [ "$want" = "$got" ] || { echo "blob mismatch $3" >> "$receipt"; exit 2; }
  echo "# $3 blob $got" >> "$receipt"
}
for f in tb/verilator/gptp_shadow/Makefile tb/verilator/gptp_shadow/gptp_shadow_wrap.sv \
         tb/verilator/gptp_shadow/sim_main.cpp \
         tb/common/verilator_harness.hpp tb/common/gptp_tx_flags.hpp \
         hdl/ieee8021as/ptp_timestamp/timestamp_counter.sv \
         hdl/ieee8021as/ptp_timestamp/KL_ptp_clock_validity.sv \
         hdl/ieee8021as/gptp_plane/KL_gptp_txticket.sv \
         hdl/ieee8021as/gptp_plane/KL_gptp_txret.sv \
         hdl/ieee8021as/gptp_plane/KL_gptp_gmii_launch.sv \
         hdl/ieee8021as/gptp_plane/KL_gptp_shadow.sv \
         hdl/common/KL_link_guard.sv hdl/common/cdc_pulse.sv hdl/common/cdc_handshake.sv; do
  fetch kebag-logic/milan-fpga "$prev" "$f" parent-tree.txt "$f"
done
fetch alexforencich/verilog-axis "$axis_pin" rtl/axis_fifo.v axis-tree.txt \
  third_party/verilog-axis/rtl/axis_fifo.v
mkdir -p gptp-processor
git -C "$clone" archive "$drev" | tar -x -C gptp-processor
if [ -n "$patch" ]; then patch -p1 < "$patch" >> "$receipt" 2>&1; fi
cd tb/verilator/gptp_shadow
set +e; make run >> "$receipt" 2>&1; rc=$?; set -e
echo "# exit: $rc" >> "$receipt"
grep -E 'checks:|^# exit|WEDGE-END' "$receipt" || true
