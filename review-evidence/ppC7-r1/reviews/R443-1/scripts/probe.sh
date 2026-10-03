#!/usr/bin/env bash
# Disposable fault probe: copy the exact-head tree, apply one sed edit to one file,
# confirm the edit landed, build the pp_top default model and run ALL of its sections.
# usage: probe.sh <name> <src-tree> <file> <sed-expr> <out-dir>
set -uo pipefail
name=$1; src=$2; file=$3; expr=$4; out=$5
w=$out/$name; rm -rf "$w"; mkdir -p "$w"
cp -a "$src/hdl" "$w/hdl"; mkdir -p "$w/tb"; cp -a "$src/tb/common" "$src/tb/pp_top" "$w/tb/"
rm -rf "$w"/tb/pp_top/obj_* "$w"/tb/pp_top/*.hex
sed -i "$expr" "$w/$file"
if cmp -s "$src/$file" "$w/$file"; then echo "PROBE $name: EDIT DID NOT APPLY"; exit 3; fi
diff -u "$src/$file" "$w/$file" | sed "s#$w/##; s#$src/##"
cd "$w/tb/pp_top" && make gsi-build > build.log 2>&1 || { echo "PROBE $name: BUILD FAILED"; tail -20 build.log; exit 4; }
./obj_dir/Vpp_top_sim "${PROBE_ARGS:-}" > run.log 2>&1; rc=$?
echo "PROBE $name: sim rc=$rc"
grep -E '^FAIL' run.log | head -40
grep -E 'checks, [0-9]+ failures|checks: ' run.log | tail -3
