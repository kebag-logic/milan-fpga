#!/usr/bin/env bash
# SPDX-License-Identifier: MIT
# Reviewer-owned whole-gate resolver mutants (R227-2, issue #504 / PR #521).
#
# For each mutant: a disposable shared clone of the reviewed head under
# $SCRATCH, the three required submodules initialised from the reviewed clone's local module repositories, one exact edit to
# sw/builder/test_builder.py (applied by resolver_gate_mutant_edit.py), then
# the PR's own compiled gate 1b through test_firmware_compiler.py with a
# verified SDK prefix. KILLED = the gate exits non-zero.
#
# Usage: resolver_gate_mutants.sh <reviewed-clone> <sdk-prefix> <scratch> <receipts> <mutant-id>...
set -euo pipefail
clone=$1 sdk=$2 scratch=$3 receipts=$4
shift 4
here=$(cd -- "$(dirname -- "$0")" && pwd)
head=$(git -C "$clone" rev-parse HEAD)
for id in "$@"; do
  (
    work="$scratch/gate-$id"
    rm -rf "$work"
    git clone --quiet --shared --no-checkout "$clone" "$work"
    git -C "$work" checkout --quiet --detach "$head"
    for sub in third_party/verilog-axis protocol-processor gptp-processor; do
      git -C "$work" config "submodule.$sub.url" "$clone/.git/modules/$sub"
    done
    git -C "$work" -c protocol.file.allow=always submodule --quiet update --init \
      third_party/verilog-axis protocol-processor gptp-processor
    git -C "$work" submodule status third_party/verilog-axis protocol-processor gptp-processor \
      > "$work/.submodule-status"
    python3 "$here/resolver_gate_mutant_edit.py" "$work/sw/builder/test_builder.py" "$id"
    git -C "$work" diff --stat -- sw/builder/test_builder.py > "$receipts/gate-$id.diffstat"
    git -C "$work" diff -- sw/builder/test_builder.py > "$receipts/gate-$id.diff"
    set +e
    (cd "$work" && python3 -u sw/builder/test_firmware_compiler.py \
        --sdk-destination "$sdk" --audit "$work/argv.jsonl") \
        > "$receipts/gate-$id.log" 2>&1
    status=$?
    set -e
    verdict=SURVIVED
    [ "$status" -ne 0 ] && verdict=KILLED
    echo "$verdict $id exit=$status" > "$receipts/gate-$id.verdict"
  ) &
done
wait
cat "$receipts"/gate-*.verdict
