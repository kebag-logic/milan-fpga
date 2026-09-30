#!/usr/bin/env bash
# Disposable probe: copy an exported head tree, apply one reviewer patch,
# build tb/pp_top (Verilator build capped at -j 8) and run the focused
# `--aecp-dispatch-only` leg and the full default leg. Prints each leg's tally
# and every FAIL line. Never touches the review clone.
# Usage: probe_mutant.sh <exported-head-tree> <patch> <work-dir>
set -euo pipefail
src=$1; patch=$2; work=$3
rm -rf "$work"; mkdir -p "$work"
cp -a "$src/hdl" "$src/tb" "$src/scripts" "$work/"
( cd "$work" && git apply --check "$patch" && git apply "$patch" )
cd "$work/tb/pp_top"
rm -rf obj_dir obj_vid ucode.hex ltn_rom.hex
sed -i 's/--build -j 0 /--build -j 8 /' Makefile
make gsi-build > build.log 2>&1 || { echo "BUILD FAILED"; tail -20 build.log; exit 3; }
set +e
./obj_dir/Vpp_top_sim --aecp-dispatch-only > aecp.log 2>&1; a=$?
./obj_dir/Vpp_top_sim > full.log 2>&1; f=$?
set -e
echo "aecp-dispatch-only rc=$a: $(grep '^\[build' aecp.log)"
grep '^FAIL' aecp.log | head -20 || true
echo "full default rc=$f: $(grep '^\[build' full.log)"
grep '^FAIL' full.log | head -20 || true
