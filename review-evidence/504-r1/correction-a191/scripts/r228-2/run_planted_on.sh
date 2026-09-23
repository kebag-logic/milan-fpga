#!/usr/bin/env bash
# SPDX-License-Identifier: MIT
# Reviewer-owned: plant one firmware edit into a copy of an arbitrary source
# tree (e.g. a resolver-mutated copy) and run its gate 1b with the SDK mapped.
# Usage: run_planted_on.sh <source-tree> <label> <scratch> <sdk> <mutant-id> <out-dir>
set -euo pipefail
src=$1 label=$2 scratch=$3 sdk=$4 mutant=$5 out=$6
here=$(cd -- "$(dirname -- "$0")" && pwd)
copy="$scratch/e2e-$label-$mutant"
python3 "$here/plant_firmware.py" "$src" "$copy" "$mutant"
git -C "$copy" diff > "$out/$label-$mutant.diff"
set +e
( cd "$copy" && python3 -u sw/builder/test_firmware_compiler.py \
    --sdk-destination "$sdk" --audit "$scratch/$label-$mutant-argv.jsonl" ) \
    > "$out/$label-$mutant.log" 2>&1
status=$?
set -e
echo "exit=$status" >> "$out/$label-$mutant.log"
echo "$label $mutant exit=$status"
