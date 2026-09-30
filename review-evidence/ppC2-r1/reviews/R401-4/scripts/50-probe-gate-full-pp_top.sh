#!/usr/bin/env bash
# Probe: C3's gate-enable-dropped patch under the FULL default pp_top run at the merged head,
# to test tb/adp_engine/README.md's record ("fails these 3 and D3R14, 4 in all") after the MAAP lane joins.
# Usage: 50-probe-gate-full-pp_top.sh <scratch-dir> <receipt-dir>
set -uo pipefail
S=${1:?}; O=${2:?}
export PATH="$S/bin:$PATH" TMPDIR="$S/tmp"
rm -rf "$S/probe-gate"; mkdir -p "$S/probe-gate"
(cd "$S/tree" && tar --exclude='obj_*' -cf - hdl tb/pp_top tb/common tb/adp_engine/mutations scripts) | tar -xf - -C "$S/probe-gate"
cd "$S/probe-gate" && git apply tb/adp_engine/mutations/gate-enable-dropped.patch && echo "planted gate-enable-dropped"
taskset -c 0-7 make -C tb/pp_top >"$O/50-gate-full-pp_top.log" 2>&1; rc=$?
echo "rc=$rc"
grep -E '^FAIL:' "$O/50-gate-full-pp_top.log" | cut -c1-160
grep -E 'checks: [0-9]+ PASS|\] [0-9]+ checks, [0-9]+ failures' "$O/50-gate-full-pp_top.log"
