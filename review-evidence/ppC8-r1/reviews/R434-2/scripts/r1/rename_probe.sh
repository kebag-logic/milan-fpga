#!/bin/sh
# Rename one bound object_name in milan_min.json (both the name table and the
# descriptor) in a disposable copy and run the gate: the digest excludes
# object_name (IEEE 1722.1-2021 6.2.2.8), so the gate must stay green.
# Usage: rename_probe.sh <head-tree> <work-dir>
set -eu
T="$2/rename-both"; rm -rf "$T"; mkdir -p "$T/hdl/aecp" "$T/tb"
cp -a "$1/hdl/aecp/desc" "$T/hdl/aecp/"; cp -a "$1/tb/desc_store" "$T/tb/"
sed -i 's/"Output 2"/"Output Two"/g' "$T/hdl/aecp/desc/milan_min.json"
cd "$T/tb/desc_store" && python3 -B test_gen_desc_image.py
