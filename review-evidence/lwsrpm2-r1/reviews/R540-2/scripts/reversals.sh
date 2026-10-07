#!/bin/bash
# Run the author's full reversal driver for both profiles concurrently in scratch copies.
set -u
. "$(dirname "$0")/env.sh"
R=$PKT/receipts/reversals; mkdir -p "$R"
for m in OFF ON; do
  W=$PKT/scratch/rev-$m; rm -rf "$W"
  ( cd "$SRC" && python3 tests/check_reversals.py --work-dir "$W" --prefix "$CGREEN_PREFIX" --milan $m > "$R/reversals-$m.log" 2>&1; echo $? > "$R/reversals-$m.rc" ) &
done
wait
for m in OFF ON; do echo "$m rc=$(cat $R/reversals-$m.rc) killed=$(grep -c '^KILLED' $R/reversals-$m.log) survived=$(grep -c '^SURVIVED\|^FAIL' $R/reversals-$m.log)"; tail -1 $R/reversals-$m.log; done
