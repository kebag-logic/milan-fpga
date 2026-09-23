#!/usr/bin/env bash
# SPDX-License-Identifier: MIT
# Reviewer-owned: plant one firmware edit into a disposable copy and run the
# head's gate 1b with the selected SDK mapped at the absolute selector.
# Usage: run_planted.sh <checkout> <scratch> <sdk-destination> <mutant-id> <out-dir>
set -euo pipefail
checkout=$1 scratch=$2 sdk=$3 mutant=$4 out=$5
here=$(cd -- "$(dirname -- "$0")" && pwd)
copy="$scratch/e2e-$mutant"
python3 "$here/plant_firmware.py" "$checkout" "$copy" "$mutant"
git -C "$copy" diff --stat > "$out/$mutant.diffstat"
git -C "$copy" diff > "$out/$mutant.diff"
set +e
( cd "$copy" && python3 -u sw/builder/test_firmware_compiler.py \
    --sdk-destination "$sdk" --audit "$scratch/$mutant-argv.jsonl" ) \
    > "$out/$mutant.log" 2>&1
status=$?
set -e
echo "exit=$status" >> "$out/$mutant.log"
echo "$mutant exit=$status"
