#!/usr/bin/env bash
# Export a git revision of the processor repository into a scratch tree and
# run the ACMP, MAAP, SRP and integration suites there, one at a time.
# Usage: run_focused_suites.sh <repo> <rev> <scratch-dir> <receipt-file>
# Needs PINNED_VERILATOR (the pinned Verilator 5.050 wrapper).
set -euo pipefail
repo=$1 rev=$2 work=$3 receipt=$4
here=$(cd "$(dirname "$0")" && pwd)
: "${PINNED_VERILATOR:?set PINNED_VERILATOR}"
"$PINNED_VERILATOR" --version | grep -q '^Verilator 5\.050 ' \
  || { echo "pinned tool is not Verilator 5.050"; exit 2; }
rm -rf "$work"; mkdir -p "$work"
git -C "$repo" archive "$rev" | tar -x -C "$work"
suites="acmp_talker acmp_listener acmp_nvm lsn_admit maap srp_admission \
srp_decoder srp_encoder srp_stream_fsms srp_top pp_top"
{
  echo "rev $(git -C "$repo" rev-parse "$rev")"
  echo "tree $(git -C "$repo" rev-parse "$rev^{tree}")"
  "$PINNED_VERILATOR" --version
  fails=0
  for s in $suites; do
    log="$work/$s.log"
    if make -C "$work/tb/$s" VERILATOR="$here/verilator_j8.sh" >"$log" 2>&1; then
      echo "PASS $s ($(grep -Eo '[0-9]+ checks: [0-9]+ PASS, [0-9]+ FAIL' "$log" | tail -1))"
    else
      echo "FAIL $s"; grep -E '^FAIL' "$log" | head -20 | sed 's/^/    /'
      tail -3 "$log" | sed 's/^/    /'; fails=$((fails + 1))
    fi
  done
  echo "focused suites failing: $fails"
} | tee "$receipt"
