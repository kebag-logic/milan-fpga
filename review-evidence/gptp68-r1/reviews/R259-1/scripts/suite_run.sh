#!/bin/bash
# SPDX-License-Identifier: CERN-OHL-W-2.0
# One donor suite's `run` target at a donor checkout, Verilator build jobs
# capped at 8. Usage: suite_run.sh <donor checkout> <suite dir> <log>
set -euo pipefail
. "$(dirname "$0")/env.sh"
cd "$1/$2"
db="$(make -pn run 2>/dev/null || true)"
VF="$(printf '%s\n' "$db" | sed -n 's/^VFLAGS = //p' | sed -n '1{s/-j 0/-j 8/;p}')"
rm -rf obj_dir gptp_ucode.hex
rc=0; make run VFLAGS="$VF" > "$3.raw" 2>&1 || rc=$?
grep -E 'gptp_ucode.hex:|checks:|^FAIL|Verilator 5' "$3.raw" > "$3" || true
rm -f "$3.raw"; echo "exit $rc" >> "$3"; exit $rc
