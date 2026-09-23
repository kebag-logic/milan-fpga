#!/usr/bin/env bash
# SPDX-License-Identifier: MIT
# Reviewer-owned: the same planted edit, graded by the SOURCE BASE's gate 1b
# (483a133e) with the head's installer/helper copied in untracked, so the
# pre-fix resolver answers with the same selected SDK.
# Usage: run_planted_base.sh <base-copy> <scratch> <sdk-destination> <mutant-id> <out-dir>
set -euo pipefail
base=$1 scratch=$2 sdk=$3 mutant=$4 out=$5
here=$(cd -- "$(dirname -- "$0")" && pwd)
copy="$scratch/e2e-base-$mutant"
python3 "$here/plant_firmware.py" "$base" "$copy" "$mutant"
git -C "$copy" rev-parse HEAD > "$out/$mutant.base-head"
git -C "$copy" diff > "$out/$mutant.diff"
set +e
( cd "$copy" && python3 -u sw/builder/test_firmware_compiler.py \
    --sdk-destination "$sdk" --audit "$scratch/base-$mutant-argv.jsonl" ) \
    > "$out/$mutant.log" 2>&1
status=$?
set -e
echo "exit=$status" >> "$out/$mutant.log"
echo "$mutant exit=$status"
