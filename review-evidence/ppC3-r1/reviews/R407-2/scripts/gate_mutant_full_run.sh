#!/usr/bin/env bash
# Disposable: full default tb/pp_top run with the gate-enable-dropped patch planted
# in a git-archive export of the exact head; lists every failing check.
set -uo pipefail
source "$(dirname "$0")/env.sh"
T="$PKT/scratch/gate-full"; rm -rf "$T"; mkdir -p "$T"
git -C "$CLONE" archive 20ec92b7b190d03c46e40be89d236bc9a0702a59 | tar -x -C "$T"
(cd "$T" && git apply "$CLONE/tb/adp_engine/mutations/gate-enable-dropped.patch") || { echo "patch refused"; exit 3; }
cd "$T/tb/pp_top"; $CAP make run > "$PKT/receipts/gate_full_run.log" 2>&1; echo "make rc=$?" >> "$PKT/receipts/gate_full_run.log"
grep -E '^FAIL:|checks, [0-9]+ failures|^make rc' "$PKT/receipts/gate_full_run.log"
