#!/bin/bash
# run_target.sh <dir> <target> <tag> : `make <target>` in <dir> with the pinned
# Verilator; log and rc under receipts/runs/<tag>.{log,rc}.
set -u
P=$REVIEWS/pp69-r512-1-packet
dir=$1; target=$2; tag=$3
cd "$dir" || exit 2
start=$(date +%s)
make "$target" VERILATOR=$P/scripts/vl_j8.sh >"$P/receipts/runs/$tag.log" 2>&1
echo "rc=$? seconds=$(( $(date +%s) - start ))" > "$P/receipts/runs/$tag.rc"
