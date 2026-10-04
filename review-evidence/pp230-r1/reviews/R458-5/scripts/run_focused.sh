#!/bin/sh
# Focused head runs for the R458-5 review of PR #154 (#230).
# usage: run_focused.sh <exported-tree> <receipt-dir> <job>
#   job: walk | store | admission | campaign | lint | check | pp_top
# VERILATOR must name the pinned 5.050 wrapper. Each job writes <job>.log
# and <job>.rc in <receipt-dir>.
set -u
tree=$1; out=$2; job=$3
: "${VERILATOR:?set VERILATOR to the pinned Verilator}"
export VERILATOR
mkdir -p "$out"
case $job in
  walk)      (cd "$tree/tb/srp_stream_fsms" && make) ;;
  store)     (cd "$tree/tb/srp_top" && make) ;;
  admission) (cd "$tree/tb/srp_admission" && make) ;;
  campaign)  (cd "$tree/tb/srp_top" && TMPDIR="${CAMPAIGN_TMP:-$TMPDIR}" \
               python3 mutants.py --output "$out/campaign-receipts" --jobs "${JOBS:-8}") ;;
  lint)      (cd "$tree" && ./scripts/lint_hdl.sh) ;;
  check)     (cd "$tree" && make check) ;;
  pp_top)    (cd "$tree/tb/pp_top" && make) ;;
  *) echo "unknown job $job" >&2; exit 2 ;;
esac > "$out/$job.log" 2>&1
rc=$?
echo "$rc" > "$out/$job.rc"
exit "$rc"
