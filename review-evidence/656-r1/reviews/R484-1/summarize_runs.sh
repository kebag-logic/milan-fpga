#!/bin/sh
# R484-1 receipt extractor: tallies, per-window order results, binary hashes
# and run times from the three scratch runs (H = exact head, C1 = head with
# A2-a removed, C2 = head RTL with the parent's axis-paced talker).
# Usage: sh summarize_runs.sh <scratch dir>
S=${1:-scratch}
for v in H C1 C2; do
  echo "== $v start=$(cat "$S/$v.start" 2>/dev/null) end=$(cat "$S/$v.end" 2>/dev/null) make_rc=$(cat "$S/$v.rc" 2>/dev/null)"
  grep -m1 '^Verilator ' "$S/$v.log"
  grep -E '^[0-9a-f]{64}  (obj_ax1x1gptp/|gptp_ax1x1_ucode)' "$S/$v.log"
  grep -E '^AUDIO (arm|result)|\[FAIL\]|^== ax1x1gptp|^AUDIO comparisons|^simulated_duration|^wall_clock|^driver_wall|^exit_status' "$S/$v.log"
done
