#!/bin/bash
# SPDX-License-Identifier: CERN-OHL-W-2.0
# Donor engine suite (`make run`: shipping + both seeded images) at a donor
# checkout, Verilator build jobs capped at 8. Usage: engine_suite_run.sh <donor checkout> <log>
set -euo pipefail
. "$(dirname "$0")/env.sh"
cd "$1/tb/verilator/engine"
db="$(make -pn run 2>/dev/null || true)"
VF="$(printf '%s\n' "$db" | sed -n 's/^VFLAGS = //p' | sed -n '1{s/-j 0/-j 8/;p}')"
rm -rf obj_dir seedrun syncseedrun gptp_ucode.hex
rc=0; make run VFLAGS="$VF" > "$2.raw" 2>&1 || rc=$?
grep -E 'gptp_ucode.hex:|^legs:|checks:|^FAIL|^-- again|Verilator 5' "$2.raw" > "$2" || true
rm -f "$2.raw"; echo "exit $rc" >> "$2"; exit $rc
