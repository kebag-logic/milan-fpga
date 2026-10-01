#!/usr/bin/env bash
# Reviewer probe: build and run tb/pp_top section AX alone at a chosen legal
# DESC_LINE_BYTES_P (the bench's own line build, `make aecp-line`, with
# LINE_FIXTURE overridden) in a disposable copy of an exported tree.
# usage: probe_line_build.sh <exported-tree> <line-bytes> <scratch-dir>
# (put the pinned Verilator wrapper first on PATH as `verilator`)
set -euo pipefail
tree=$1; line=$2; work=$3/probe-line$line
rm -rf "$work"; mkdir -p "$work/tb"
cp -r "$tree/hdl" "$work/"
cp -r "$tree/tb/common" "$tree/tb/pp_top" "$work/tb/"
rm -rf "$work/tb/pp_top"/obj_* "$work/tb/pp_top"/*.hex
make -C "$work/tb/pp_top" aecp-line LINE_FIXTURE="$line"
