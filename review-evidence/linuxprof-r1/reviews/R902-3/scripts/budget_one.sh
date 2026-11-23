#!/usr/bin/env bash
# budget_one.sh <tree> <tag> <name> <timeout-s> <script> [args...]: one service-budget command in an extracted tree.
# Writes receipts/budget_<name>_<tag>.txt (tree path masked as <TREE>) with rc and seconds.
set -u
tree=$1 tag=$2 name=$3 limit=$4; shift 4; out=${OUT:?}
f="$out/budget_${name}_${tag}.txt"; t0=$(date +%s)
echo "\$ (tree $tag) python3 -B tb/verilator/ctrl_service_budget/$*" > "$f"
(cd "$tree" && PYTHONDONTWRITEBYTECODE=1 timeout "$limit" python3 -B "tb/verilator/ctrl_service_budget/$@") > "$f.raw" 2>&1; rc=$?
sed "s#$tree#<TREE>#g" "$f.raw" >> "$f"; rm -f "$f.raw"
echo "rc=$rc seconds=$(( $(date +%s) - t0 ))" >> "$f"
