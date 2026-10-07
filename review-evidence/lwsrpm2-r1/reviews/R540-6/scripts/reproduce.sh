#!/bin/sh
# SPDX-License-Identifier: Apache-2.0
# Portable driver for this packet. REVIEW_SOURCE: exact-head checkout. Requires the
# unit framework built under scratch/prefix (cgreen 1.7.0, commit feeb85ed) and the
# prior public probes fetched into scratch/ev/reviews/{R541-5,R540-5}/scripts/.
set -eu
: "${REVIEW_SOURCE:?}"
PKT=$(cd "$(dirname "$0")/.." && pwd); export SCRATCH="$PKT/scratch" PKT_SCRIPTS="$PKT/scripts" PYTHONDONTWRITEBYTECODE=1
S="$PKT/scripts"; P="$SCRATCH/prefix"
for m in OFF ON; do
  "$S/run_bg.sh" profile-$m "$S/profile.sh" $m
  "$S/run_bg.sh" reversals-$m env LD_LIBRARY_PATH="$P/lib" python3 "$REVIEW_SOURCE/tests/check_reversals.py" --work-dir "$SCRATCH/rev-$m" --prefix "$P" --milan $m
done
"$S/wait_rc.sh" 3000 profile-OFF profile-ON
for m in OFF ON; do
  "$S/run_probe.sh" $m "$SCRATCH/build-$m" r540-probe-$m
  cc -std=c11 -I"$REVIEW_SOURCE/src/include" -I"$REVIEW_SOURCE/src" -I"$REVIEW_SOURCE/tests/unit" "$SCRATCH/ev/reviews/R541-5/scripts/probe.c" "$REVIEW_SOURCE/tests/unit/fault_alloc.c" -L"$SCRATCH/build-$m" -Wl,-rpath,"$SCRATCH/build-$m" -lshlan -o "$SCRATCH/r541probe-$m"
  "$SCRATCH/r541probe-$m" cross-port > "$PKT/receipts/r541-cross-port-$m.log" 2>&1 || true
  "$SCRATCH/r541probe-$m" > "$PKT/receipts/r541-probe-$m.log" 2>&1 || true
  "$S/run_bg.sh" sanitize-$m "$S/sanitize.sh" $m
done
for M in 0 1; do sh "$SCRATCH/ev/reviews/R540-5/scripts/run_probe.sh" "$REVIEW_SOURCE" "$SCRATCH/probe_r5" $M > "$PKT/receipts/r540-5-probe-$M.log" 2>&1 || true; done
python3 "$S/mutants.py" --set round7 --jobs 8 > "$PKT/receipts/mutants.log" 2>&1
python3 "$S/mutants.py" --set prior --jobs 4 > "$PKT/receipts/prior-plants.log" 2>&1
"$S/wait_rc.sh" 3000 reversals-OFF reversals-ON sanitize-OFF sanitize-ON
